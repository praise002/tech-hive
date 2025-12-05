import logging
import uuid
from datetime import timedelta
from decimal import Decimal
from typing import Any, Dict, Optional, Tuple

from apps.subscriptions.choices import (
    StatusChoices,
    SubscriptionChoices,
    TransactionTypeChoices,
)
from apps.subscriptions.models import PaymentTransaction, Subscription, SubscriptionPlan
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from .paystack_service import paystack_service

User = get_user_model()
logger = logging.getLogger(__name__)


class SubscriptionService:
    """
    Handles all subscription business logic.
    """

    def start_trial(
        self, user, plan: SubscriptionPlan
    ) -> Tuple[Subscription, PaymentTransaction]:
        """
        Start a 7-day trial for a first-time user.
        No Paystack API calls are made.

        Args:
            user: User starting trial
            plan: SubscriptionPlan for the trial

        Returns:
            (Subscription, PaymentTransaction)

        Raises:
            ValueError: If user already has subscription or is not eligible for trial
        """
        try:
            # Check for active subscription
            active_subscription = user.subscription
            if active_subscription:
                raise ValueError("User already has an active subscription")

            # Check eligibility based on any previous subscriptions
            has_previous_subscription = user.subscriptions.exists()
            if has_previous_subscription:
                raise ValueError(
                    "User is not eligible for trial (previous subscription exists)"
                )

            now = timezone.now()
            trial_start = now
            trial_end = now + timedelta(days=7)
            reference = f"TXN_{uuid.uuid4().hex[:12].upper()}"

            with transaction.atomic():
                subscription = Subscription.objects.create(
                    user=user,
                    plan=plan,
                    status="TRIALING",
                    start_date=now,
                    trial_start=trial_start,
                    trial_end=trial_end,
                    # No billing periods during trial
                    current_period_start=None,
                    current_period_end=None,
                    next_billing_date=trial_end,
                )

                payment_transaction = PaymentTransaction.objects.create(
                    user=user,
                    subscription=subscription,
                    reference=reference,
                    amount=plan.price,  # Store full price even for trial
                    currency="NGN",
                    status=StatusChoices.SUCCESS,  # Trial is immediately "successful"
                    transaction_type=TransactionTypeChoices.SUBSCRIPTION,
                )

                logger.info(
                    f"Trial started for {user.email}: {plan.name} "
                    f"(expires: {trial_end.strftime('%Y-%m-%d %H:%M')})"
                )

                return subscription, payment_transaction

        except ValueError as e:
            logger.warning(f"Trial creation failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error starting trial: {str(e)}")
            raise Exception(f"Failed to start trial: {str(e)}")

    def create_subscription_after_trial(
        self, trial_subscription: Subscription
    ) -> Tuple[PaymentTransaction, str]:
        """
        Convert a trial subscription to a paid subscription.
        Called when trial period ends and user wants to continue.

        Args:
            trial_subscription: The existing trial subscription

        Returns:
            (PaymentTransaction, authorization_url)

        Raises:
            ValueError: If subscription is not a valid trial
        """
        try:
            if trial_subscription.status != "TRIALING":
                raise ValueError("Subscription is not in trial state")

            if not trial_subscription.is_trial:
                raise ValueError("Subscription was not a trial")

            now = timezone.now()
            if now < trial_subscription.trial_end:
                logger.warning(
                    f"Trial has not yet ended for {trial_subscription.user.email}. "
                    f"Proceeding with early conversion."
                )

            # Prepare metadata
            metadata = {
                "user_id": str(trial_subscription.user.id),
                "user_email": trial_subscription.user.email,
                "plan_id": str(trial_subscription.plan.id),
                "plan_name": trial_subscription.plan.name,
                "subscription_id": str(trial_subscription.id),
            }

            with transaction.atomic():
                # Initialize Paystack transaction for the trial conversion
                paystack_response = paystack_service.initialize_transaction(
                    email=trial_subscription.user.email,
                    amount=trial_subscription.plan.price,
                    plan_code=trial_subscription.plan.paystack_plan_code,
                    callback_url=f"{self._get_frontend_url()}/payment/callback",
                    metadata=metadata,
                    reference=trial_subscription.reference,
                )
                # Create payment transaction record
                payment_transaction = PaymentTransaction.objects.create(
                    user=trial_subscription.user,
                    subscription=trial_subscription,
                    reference=trial_subscription.reference,
                    paystack_reference=paystack_response.get("reference"),
                    amount=trial_subscription.plan.price,
                    currency="NGN",
                    transaction_type=TransactionTypeChoices.SUBSCRIPTION,
                )

                authorization_url = paystack_response.get("authorization_url", "")

                logger.info(
                    f"Trial conversion initiated for {trial_subscription.user.email}: "
                    f"{trial_subscription.plan.name} (reference: {trial_subscription.reference})"
                )

                return payment_transaction, authorization_url

        except ValueError as e:
            logger.warning(f"Trial conversion failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error converting trial: {str(e)}")
            raise Exception(f"Failed to convert trial: {str(e)}")

    def create_paid_subscription(
        self, user, plan: SubscriptionPlan, has_trial: bool = True
    ) -> Tuple[Subscription, PaymentTransaction, str]:
        """
        Create an immediate paid subscription (no trial).
        Makes Paystack API calls for payment processing.

        Args:
            user: User subscribing
            plan: SubscriptionPlan to subscribe to


        Returns:
            (Subscription, PaymentTransaction, authorization_url)

        Raises:
            ValueError: If user already has active subscription
            Exception: If Paystack initialization fails
        """
        try:
            existing = user.subscription
            if existing and existing.is_active:
                raise ValueError("User already has an active subscription")

            # Generate unique reference
            reference = f"TXN_{uuid.uuid4().hex[:12].upper()}"

            # Determine amount (0 for trial, full price otherwise)
            amount = plan.price

            # Calculate dates
            now = timezone.now()

            # Prepare metadata
            metadata = {
                "user_id": str(user.id),
                "user_email": user.email,
                "plan_id": str(plan.id),
                "plan_name": plan.name,
            }

            with transaction.atomic():
                subscription = Subscription.objects.create(
                    user=user,
                    plan=plan,
                    start_date=now,
                    # No trial for immediate subscriptions
                    trial_start=None,
                    trial_end=None,
                    # Billing periods will be set by webhook after payment
                    current_period_start=None,
                    current_period_end=None,
                    next_billing_date=None,
                )
                metadata["subscription_id"] = str(subscription.id)

                paystack_response = paystack_service.initialize_transaction(
                    email=user.email,
                    amount=amount,
                    plan_code=plan.paystack_plan_code,
                    callback_url=f"{self._get_frontend_url()}/payment/callback",
                    metadata=metadata,
                    reference=reference,
                )

                # Create PaymentTransaction record
                payment_transaction = PaymentTransaction.objects.create(
                    user=user,
                    subscription=subscription,
                    reference=reference,
                    paystack_reference=paystack_response["reference"],
                    amount=plan.price,  # Store full price even for trial
                    currency="NGN",
                    transaction_type=TransactionTypeChoices.SUBSCRIPTION,
                )

                logger.info(
                    f"Subscription initialized for {user.email}: "
                    f"{plan.name} (Trial: {has_trial})"
                )

                return (
                    subscription,
                    payment_transaction,
                    paystack_response["authorization_url"],
                )

        except ValueError as e:
            logger.warning(f"Subscription creation failed: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Error creating subscription: {str(e)}")
            raise Exception(f"Failed to create subscription: {str(e)}")

    def verify_and_activate_subscription(
        self, reference: str
    ) -> Tuple[bool, str, Optional[Subscription]]:
        """
        Verify payment and activate subscription.

        Args:
            reference: Transaction reference

        Returns:
            (success: bool, message: str, subscription: Optional[Subscription])
        """
        try:
            # Find payment transaction
            try:
                payment_transaction = PaymentTransaction.objects.get(
                    reference=reference
                )
            except PaymentTransaction.DoesNotExist:
                logger.error(f"Transaction not found: {reference}")
                return False, "Transaction not found", None

            # Check if already processed
            if payment_transaction.status == StatusChoices.SUCCESS:
                logger.info(f"Transaction already processed: {reference}")
                return True, "Already processed", payment_transaction.subscription

            # Verify with Paystack
            paystack_data = paystack_service.verify_transaction(reference)

            if paystack_data["status"] != "success":
                # Payment failed
                payment_transaction.mark_as_failed(
                    reason=paystack_data.get("gateway_response", "Payment failed"),
                    paystack_response=paystack_data,
                )

                # Delete subscription if exists
                if payment_transaction.subscription:
                    payment_transaction.subscription.delete()

                logger.warning(f"Payment verification failed: {reference}")
                return False, "Payment failed", None

            # Payment successful
            with transaction.atomic():
                subscription = payment_transaction.subscription

                # Update subscription with Paystack data
                authorization = paystack_data.get("authorization", {})
                customer = paystack_data.get("customer", {})

                subscription.paystack_customer_code = customer.get("customer_code")
                subscription.paystack_authorization_code = authorization.get(
                    "authorization_code"
                )
                subscription.card_last4 = authorization.get("last4")
                subscription.card_type = authorization.get("card_type")
                subscription.card_bank = authorization.get("bank")
                subscription.save()

                # Mark transaction as successful
                payment_transaction.mark_as_success(paystack_response=paystack_data)

                logger.info(f"Subscription activated: {subscription.user.email}")

                return True, "Subscription activated", subscription

        except Exception as e:
            logger.error(f"Error verifying subscription: {str(e)}")
            return False, str(e), None

    # ===== Payment Processing =====

    def process_successful_payment(
        self,
        subscription: Subscription,
        transaction_data: Dict,
        transaction_type: str = "RENEWAL",
        period_start: Optional[str] = None,
        period_end: Optional[str] = None,
        next_billing_date: Optional[str] = None,
    ) -> PaymentTransaction:
        """
        Process a successful payment.

        Args:
            subscription: Subscription that was paid
            transaction_data: Data from Paystack
            transaction_type: Type of transaction
            period_start: Period start from Paystack (ISO format)
            period_end: Period end from Paystack (ISO format)
            next_billing_date: Next billing date from Paystack (ISO format)


        Returns:
            PaymentTransaction record
        """
        try:
            with transaction.atomic():
                # Create payment transaction record
                payment_transaction = PaymentTransaction.objects.create(
                    user=subscription.user,
                    subscription=subscription,
                    reference=f"TXN_{uuid.uuid4().hex[:12].upper()}",
                    paystack_reference=transaction_data.get("reference"),
                    amount=Decimal(transaction_data.get("amount", 0))
                    / Decimal("100"),  # Convert from kobo
                    currency=transaction_data.get("currency", "NGN"),
                    status="SUCCESS",
                    transaction_type=transaction_type,
                    paid_at=timezone.now(),
                    paystack_response=transaction_data,
                )

                # Update subscription
                if subscription.status == SubscriptionChoices.TRIALING:
                    # Trial ended, now active
                    subscription.status = "ACTIVE"
                elif subscription.status in ["PAST_DUE", "EXPIRED"]:
                    # Recovered from failed payment
                    subscription.status = "ACTIVE"

                # Update billing dates - use Paystack data if available (it is being returned in invoice.update)
                if period_start and period_end and next_billing_date:
                    subscription.current_period_start = parse_datetime(period_start)
                    subscription.current_period_end = parse_datetime(period_end)
                    subscription.next_billing_date = parse_datetime(next_billing_date)

                    logger.info(
                        f"Updated billing periods from Paystack for {subscription.user.email}: "
                        f"{period_start} to {period_end}, next: {next_billing_date}"
                    )
                else:
                    # TODO: FIGURE OUT A WAY TO FIX LATER FOR FIRST SUBSCRIPTION
                    # Fallback to manual calculation (for initial payments without invoice data and for first subscription that doesn't return invoice.update)
                    now = timezone.now()
                    subscription.current_period_start = now
                    subscription.current_period_end = now + timedelta(days=30)
                    subscription.next_billing_date = subscription.current_period_end

                    logger.info(
                        f"Using manual billing calculation for {subscription.user.email} "
                        f"(no Paystack period data available)"
                    )

                # Reset retry tracking
                subscription.retry_count = 0
                subscription.payment_failed_at = None
                subscription.last_retry_at = None

                subscription.save()

                logger.info(
                    f"Payment processed successfully for {subscription.user.email}: "
                    f"₦{payment_transaction.amount}"
                )

                return payment_transaction

        except Exception as e:
            logger.error(f"Error processing successful payment: {str(e)}")
            raise

    def process_failed_payment(
        self,
        subscription: Subscription,
        failure_reason: str,
        transaction_data: Optional[Dict] = None,
    ) -> PaymentTransaction:
        """
        Process a failed payment.

        Args:
            subscription: Subscription with failed payment
            failure_reason: Why payment failed
            transaction_data: Optional Paystack data

        Returns:
            PaymentTransaction record
        """
        try:
            with transaction.atomic():
                # Create failed transaction record
                payment_transaction = PaymentTransaction.objects.create(
                    user=subscription.user,
                    subscription=subscription,
                    reference=f"TXN_{uuid.uuid4().hex[:12].upper()}",
                    paystack_reference=(
                        transaction_data.get("reference") if transaction_data else None
                    ),
                    amount=subscription.plan.price,
                    currency="NGN",
                    status="FAILED",
                    transaction_type="RENEWAL",
                    failed_at=timezone.now(),
                    failure_reason=failure_reason,
                    paystack_response=transaction_data,
                )

                # Update subscription
                subscription.mark_as_failed()

                logger.warning(
                    f"Payment failed for {subscription.user.email}: {failure_reason}"
                )

                return payment_transaction

        except Exception as e:
            logger.error(f"Error processing failed payment: {str(e)}")
            raise

    # ===== Payment Retry =====

    def retry_payment(
        self, subscription: Subscription, is_manual: bool = False
    ) -> Tuple[bool, str, Optional[PaymentTransaction]]:
        """
        Retry a failed payment.

        Args:
            subscription: Subscription to retry payment for
            is_manual: Whether this is a manual retry (user-initiated)

        Returns:
            (success: bool, message: str, transaction: Optional[PaymentTransaction])
        """
        try:
            if subscription.status != SubscriptionChoices.PAST_DUE:
                return False, "Subscription is not past due", None

            if not subscription.paystack_authorization_code:
                return False, "No saved payment method", None

            # Attempt to charge
            result = paystack_service.charge_authorization(
                authorization_code=subscription.paystack_authorization_code,
                email=subscription.user.email,
                amount=subscription.plan.price,
                metadata={
                    "subscription_id": str(subscription.id),
                    "retry_number": subscription.retry_count + 1,
                    "is_manual": is_manual,
                },
            )

            if result["status"]:
                # Payment successful
                transaction_data = result["data"]
                payment_transaction = self.process_successful_payment(
                    subscription=subscription,
                    transaction_data=transaction_data,
                    transaction_type="MANUAL_RETRY" if is_manual else "RETRY",
                )

                logger.info(f"Payment retry successful for {subscription.user.email}")

                return True, "Payment successful", payment_transaction

            else:
                # Payment failed
                failure_reason = result.get("message", "Payment failed")

                payment_transaction = PaymentTransaction.objects.create(
                    user=subscription.user,
                    subscription=subscription,
                    reference=f"TXN_{uuid.uuid4().hex[:12].upper()}",
                    amount=subscription.plan.price,
                    currency="NGN",
                    status="FAILED",
                    transaction_type="MANUAL_RETRY" if is_manual else "RETRY",
                    failed_at=timezone.now(),
                    failure_reason=failure_reason,
                    is_retry=True,
                    retry_number=subscription.retry_count + 1,
                )
                # TODO: last_retry_at

                # Increment retry count
                if not is_manual:
                    subscription.increment_retry_count()

                logger.warning(
                    f"Payment retry failed for {subscription.user.email}: {failure_reason}"
                )

                return False, failure_reason, payment_transaction

        except Exception as e:
            logger.error(f"Error retrying payment: {str(e)}")
            return False, str(e), None

    # ===== Subscription Management =====

    def cancel_subscription(
        self,
        subscription: Subscription,
        reason: Optional[str] = None,
    ) -> bool:  # TODO: USER CAN CALL MANUALLY OR BE CALLED WHEN GRACE PERIOD EXCEEDED
        """
        Cancel a subscription.

        Args:
            subscription: Subscription to cancel
            reason: Cancellation reason (optional)

        Returns:
            True if successful
        """
        try:
            with transaction.atomic():
                # Disable in Paystack
                if (
                    subscription.paystack_subscription_code
                    and subscription.paystack_email_token
                ):
                    try:
                        paystack_service.disable_subscription(
                            subscription_code=subscription.paystack_subscription_code,
                            email_token=subscription.paystack_email_token,
                        )
                    except Exception as e:
                        logger.warning(
                            f"Failed to disable Paystack subscription: {str(e)}"
                        )
                        return False

                # Cancel subscription
                subscription.cancel(reason=reason)

                logger.info(f"Subscription cancelled for {subscription.user.email} ")

                return True

        except Exception as e:
            logger.error(f"Error cancelling subscription: {str(e)}")
            raise

    def reactivate_subscription(self, subscription: Subscription) -> bool:
        """
        Reactivate a cancelled subscription.
        If a user does not reactivate before the period ends,
        it cannot be reactivated.

        Args:
            subscription: Subscription to reactivate

        Returns:
            True if successful

        Raises:
            ValueError: If subscription cannot be reactivated
        """
        try:
            with transaction.atomic():
                # Re-enable in Paystack
                if (
                    subscription.paystack_subscription_code
                    and subscription.paystack_email_token
                ):
                    try:
                        paystack_service.enable_subscription(
                            subscription_code=subscription.paystack_subscription_code,
                            email_token=subscription.paystack_email_token,
                        )
                    except Exception as e:
                        logger.warning(
                            f"Failed to enable Paystack subscription: {str(e)}"
                        )

                # Reactivate subscription
                subscription.reactivate()

                logger.info(f"Subscription reactivated for {subscription.user.email}")

                return True

        except ValueError as e:
            logger.warning(f"Reactivation failed: {str(e)}")
            raise

        except Exception as e:
            logger.error(f"Error reactivating subscription: {str(e)}")
            raise

    def expire_subscription(self, subscription: Subscription) -> bool:
        """
        Expire a subscription (end of period or grace period).

        Args:
            subscription: Subscription to expire

        Returns:
            True if successful
        """
        try:
            subscription.expire()

            logger.info(f"Subscription expired for {subscription.user.email}")

            return True

        except Exception as e:
            logger.error(f"Error expiring subscription: {str(e)}")
            raise

    def get_subscription_status(self, user) -> Dict:
        """Get detailed subscription status for a user."""
        try:
            subscription = user.subscription

            return {
                "has_subscription": True,
                "is_premium": subscription.is_active,
                "status": subscription.status,
                "plan": {
                    "name": subscription.plan.name,
                    "price": float(subscription.plan.price),
                    "billing_cycle": subscription.plan.billing_cycle,
                },
                "trial": {
                    "is_trial": subscription.is_trial,
                    "trial_start": subscription.trial_start,
                    "trial_end": (
                        subscription.trial_end.isoformat()
                        if subscription.trial_end
                        else None
                    ),
                },
                "billing": {
                    "current_period_start": subscription.current_period_start.isoformat(),
                    "current_period_end": subscription.current_period_end.isoformat(),
                    "next_billing_date": (
                        subscription.next_billing_date.isoformat()
                        if subscription.next_billing_date
                        else None
                    ),
                    "days_remaining": subscription.days_until_expiry,
                },
                "card": (
                    {
                        "last4": subscription.card_last4,
                        "type": subscription.card_type,
                        "bank": subscription.card_bank,
                    }
                    if subscription.card_last4
                    else None
                ),
                "cancellation": {
                    "cancelled": subscription.cancelled_at
                    is not None,  # returns a boolean
                    "cancelled_at": (
                        subscription.cancelled_at.isoformat()
                        if subscription.cancelled_at
                        else None
                    ),
                    "cancel_at_period_end": subscription.cancel_at_period_end,
                    "reason": subscription.cancel_reason,
                },
                "payment_status": {
                    "is_past_due": subscription.status == "PAST_DUE",
                    "payment_failed_at": (
                        subscription.payment_failed_at.isoformat()
                        if subscription.payment_failed_at
                        else None
                    ),
                    "retry_count": subscription.retry_count,
                    "is_in_grace_period": subscription.is_in_grace_period,
                    "grace_period_ends_at": (
                        subscription.grace_period_ends_at.isoformat()
                        if subscription.grace_period_ends_at
                        else None
                    ),
                },
            }
        except Subscription.DoesNotExist:
            return {
                "has_subscription": False,
                "is_premium": False,
                "current_plan": "Basic",
            }

    def update_payment_method(self, subscription: Subscription) -> str:
        """
        Generate secure link for user to update their payment card.

        This is used when:
        - User's card is expiring
        - Payment has failed
        - User wants to change their card

        Flow:
        1. Validate subscription has Paystack subscription code
        2. Call Paystack API to generate management link
        3. Return URL for user to visit
        4. User updates card on Paystack's hosted page
        5. New card is stored in Paystack (no webhook sent at this point)
        6. Next billing cycle: charge.success webhook will contain new card details
        7. Webhook handler updates card_last4, card_type, etc. in DB

        Args:
            subscription: The subscription to update payment method for

        Returns:
            str: URL where user can update their card

        Raises:
            ValueError: If subscription doesn't have Paystack subscription code
            Exception: If Paystack API call fails
        """
        try:

            if not subscription.paystack_subscription_code:
                error_msg = (
                    f"No Paystack subscription found for user {subscription.user.email}. "
                    f"Cannot generate update link."
                )
                logger.error(error_msg)
                raise ValueError(error_msg)

            logger.info(
                f"Generating payment update link for {subscription.user.email} "
                f"(subscription: {subscription.paystack_subscription_code})"
            )

            update_link = paystack_service.generate_update_subscription_link(
                subscription.paystack_subscription_code
            )

            logger.info(
                f"Payment update link generated successfully for {subscription.user.email}"
            )

            return update_link

        except ValueError as ve:
            logger.warning(f"Validation error generating update link: {str(ve)}")
            raise

        except Exception as e:
            logger.error(
                f"Error generating payment update link for {subscription.user.email}: {str(e)}"
            )
            raise Exception(f"Failed to generate payment update link: {str(e)}")

    def sync_plans_from_paystack(self) -> Dict[str, Any]:
        """
        Sync all subscription plans from Paystack to local database.

        This ensures your DB stays in sync with Paystack, especially useful for:
        - Initial setup (importing existing plans)
        - Regular maintenance (cron job)
        - After creating/updating plans in Paystack dashboard

        Flow:
        1. Fetch all plans from Paystack (with pagination)
        2. For each plan:
            a. Check if exists in DB (by paystack_plan_code)
            b. If exists: Update fields (name, amount, interval, etc.)
            c. If not exists: Create new SubscriptionPlan
        3. Return summary of operations

        Returns:
            {
                "success": True,
                "synced": 5,      # Total plans processed
                "created": 2,     # New plans created
                "updated": 3,     # Existing plans updated
                "errors": []      # List of any errors encountered
            }

        Example:
            # Run manually
            result = subscription_service.sync_plans_from_paystack()
            print(f"Synced {result['synced']} plans")

            # Or via cron job (daily at 2am)
            # 0 2 * * * python manage.py sync_paystack_plans
        """
        try:
            logger.info("Starting plan synchronization from Paystack...")

            # Initialize counters to track what we did
            synced_count = 0
            created_count = 0
            updated_count = 0
            errors = []

            page = 1
            per_page = 50

            while True:
                try:

                    logger.info(f"Fetching plans page {page}...")
                    result = paystack_service.list_plans(page=page, per_page=per_page)

                    plans = result["plans"]
                    meta = result["meta"]

                    # If no plans returned, we're done
                    if not plans:
                        logger.info("No more plans to sync")
                        break

                    logger.info(f"Processing {len(plans)} plans from page {page}")

                    for plan_data in plans:
                        try:
                            plan_code = plan_data["plan_code"]
                            name = plan_data["name"]
                            amount = Decimal(plan_data["amount"]) / Decimal(
                                "100"
                            )  # Convert kobo to Naira
                            interval = plan_data["interval"]
                            description = plan_data.get("description")
                            currency = plan_data.get("currency", "NGN")

                            # update_or_create is atomic - it either updates existing or creates new
                            _, created = SubscriptionPlan.objects.update_or_create(
                                # Find by: paystack_plan_code (unique identifier)
                                paystack_plan_code=plan_code,
                                # Update/Create with:
                                defaults={
                                    "name": name,
                                    "price": amount,
                                    "billing_cycle": interval,  # "monthly", "annually", etc.
                                    "description": description,
                                    "currency": currency,
                                },
                            )

                            # Track what we did
                            if created:
                                created_count += 1
                                logger.info(f"✓ Created new plan: {name} ({plan_code})")
                            else:
                                updated_count += 1
                                logger.info(
                                    f"✓ Updated existing plan: {name} ({plan_code})"
                                )

                            synced_count += 1

                        except Exception as plan_error:
                            # If one plan fails, log it but continue with others
                            error_msg = f"Failed to sync plan {plan_data.get('plan_code')}: {str(plan_error)}"
                            logger.error(error_msg)
                            errors.append(error_msg)
                            continue

                    # Check if there are more pages
                    # meta contains: {"total": 10, "page": 1, "pageCount": 2}
                    current_page = meta.get("page", page)
                    total_pages = meta.get("pageCount", 1)

                    if current_page >= total_pages:
                        # We've processed all pages
                        logger.info(f"Processed all {total_pages} pages")
                        break

                    # Move to next page
                    page += 1

                except Exception as page_error:
                    # If fetching a page fails, log and stop
                    error_msg = f"Failed to fetch page {page}: {str(page_error)}"
                    logger.error(error_msg)
                    errors.append(error_msg)
                    break

            result = {
                "success": len(errors) == 0,
                "synced": synced_count,
                "created": created_count,
                "updated": updated_count,
                "errors": errors,
            }

            logger.info(
                f"Plan sync completed: {synced_count} synced "
                f"({created_count} created, {updated_count} updated, "
                f"{len(errors)} errors)"
            )

            return result

        except Exception as e:
            logger.error(f"Fatal error during plan sync: {str(e)}")
            return {
                "success": False,
                "synced": 0,
                "created": 0,
                "updated": 0,
                "errors": [str(e)],
            }

    def create_plan(
        self,
        name: str,
        interval: str,
        amount: int,  # int for paystack, Decimal for local db
        features: str,
        description: Optional[str] = None,
        currency: str = "NGN",
    ) -> SubscriptionPlan:
        """
        Create a subscription plan in both Paystack and local database.

        Flow:
        1. Validate inputs (name not empty, valid interval, amount > 0)
        2. Create plan in Paystack first
        3. If Paystack succeeds, create in local DB
        4. If Paystack fails, don't create in DB

        Args:
            name: Plan name (e.g., "Premium Monthly")
            interval: Billing cycle - "monthly", "annually", "weekly", etc.
            amount: Price in kobo
            description: Optional description
            currency: Currency code (default: "NGN")

        Returns:
            SubscriptionPlan: The created plan instance

        Raises:
            ValueError: If validation fails
            Exception: If Paystack API call fails

        Example:
            plan = subscription_service.create_plan(
                name="Premium Monthly",
                interval="monthly",
                amount=Decimal("10000"),
                description="Full access to all premium features"
            )
            print(f"Plan created: {plan.paystack_plan_code}")
        """
        try:
            if not name or not name.strip():
                raise ValueError("Plan name cannot be empty")

            if amount <= 0:
                raise ValueError("Plan amount must be greater than 0")

            valid_intervals = [
                "monthly",
                "annually",
            ]  # based on my app logic
            if interval not in valid_intervals:
                raise ValueError(
                    f"Invalid interval '{interval}'. "
                    f"Must be one of: {', '.join(valid_intervals)}"
                )

            logger.info(f"Creating plan: {name} - {amount}kobo/{interval}")

            # This is the source of truth - if Paystack fails, we don't create locally
            paystack_response = paystack_service.create_plan(
                name=name,
                interval=interval,
                amount=amount,
                currency=currency,
                description=description,
            )

            plan_code = paystack_response["plan_code"]
            logger.info(f"Plan created in Paystack: {plan_code}")

            # Now that Paystack succeeded, we can safely create locally
            with transaction.atomic():
                plan = SubscriptionPlan.objects.create(
                    name=name,
                    price=Decimal(amount) / Decimal("100"),
                    billing_cycle=interval,
                    description=description,
                    currency=currency,
                    paystack_plan_code=plan_code,
                    features=features,
                )

            logger.info(
                f"Plan created successfully in database: {plan.name} "
                f"(ID: {plan.id}, Paystack: {plan_code})"
            )

            return plan

        except ValueError as ve:
            logger.warning(f"Validation error creating plan: {str(ve)}")
            raise

        except Exception as e:
            logger.error(f"Error creating plan '{name}': {str(e)}")
            raise Exception(f"Failed to create plan: {str(e)}")

    def update_plan(
        self, plan: SubscriptionPlan, data: Dict[str, Any]
    ) -> SubscriptionPlan:
        """
        Update a subscription plan in both Paystack and local database.

        Flow:
        1. Validate plan exists and has Paystack code
        2. Prepare update payload (convert amount to kobo if provided)
        3. Update in Paystack first
        4. If Paystack succeeds, update local DB
        5. If Paystack fails, don't update DB

        Args:
            plan: SubscriptionPlan instance to update
            data: Dictionary with fields to update:
                {
                    "name": "New Plan Name",
                    "amount": 15000,
                    "description": "Updated description",
                    "interval": "annually",
                    "update_existing_subscriptions": True
                }

        Returns:
            SubscriptionPlan: The updated plan instance

        Raises:
            ValueError: If plan doesn't have Paystack code
            Exception: If Paystack API call fails

        Example:
            plan = SubscriptionPlan.objects.get(id=1)
            updated_plan = subscription_service.update_plan(
                plan=plan,
                data={
                    "name": "Premium Plus",
                    "amount": 12000,
                }
            )
        """
        try:
            if not plan.paystack_plan_code:
                raise ValueError(
                    f"Plan '{plan.name}' has no Paystack plan code. " f"Cannot update."
                )

            logger.info(f"Updating plan: {plan.name} ({plan.paystack_plan_code})")

            paystack_data = {}

            if "name" in data:
                paystack_data["name"] = data["name"]

            if "description" in data:
                paystack_data["description"] = data["description"]

            # Convert amount from Naira to kobo if provided
            if "amount" in data:
                amount_naira = data["amount"]
                if not isinstance(amount_naira, int):
                    amount_naira = int(amount_naira)

                # Paystack expects amount in kobo (smallest currency unit)
                amount_kobo = int(amount_naira * Decimal("100"))
                paystack_data["amount"] = amount_kobo

            if "interval" in data:
                paystack_data["interval"] = data["interval"]

            # If True, all current subscribers will be affected
            # If False, only new subscribers will use new price
            if "update_existing_subscriptions" in data:
                paystack_data["update_existing_subscriptions"] = data[
                    "update_existing_subscriptions"
                ]

            logger.info(f"Updating plan in Paystack with data: {paystack_data}")

            paystack_service.update_plan(
                plan_code=plan.paystack_plan_code, data=paystack_data
            )

            logger.info(
                f"Plan updated successfully in Paystack: {plan.paystack_plan_code}"
            )

            # Now that Paystack succeeded, update our records
            with transaction.atomic():
                # Update each field if provided
                if "name" in data:
                    plan.name = data["name"]

                if "amount" in data:
                    plan.price = data["amount"]

                if "description" in data:
                    plan.description = data["description"]

                if "interval" in data:
                    plan.billing_cycle = data["interval"]

                plan.save()

            logger.info(
                f"Plan updated successfully in database: {plan.name} "
                f"(ID: {plan.id})"
            )

            return plan

        except ValueError as ve:
            logger.warning(f"Validation error updating plan: {str(ve)}")
            raise

        except Exception as e:
            logger.error(f"Error updating plan '{plan.name}': {str(e)}")
            raise Exception(f"Failed to update plan: {str(e)}")

    def _get_frontend_url(self) -> str:
        """Get frontend URL from settings."""
        return settings.FRONTEND_URL


subscription_service = SubscriptionService()

# NOTE:
# If a customer has multiple authorizations, you can select which one to use for
# the subscription, by passing the authorization_code as authorization when creating the subscription.
# Otherwise, Paystack picks the most recent authorization to charge.

# Monthly Subscription Billing
# Billing for subscriptions with a monthly interval depends on the day of the month the
# subscription was created. If the subscription was created on or before the 28th of the month,
# it gets billed on the same day, every month, for the duration of the plan. Subscriptions created on
# or between the 29th - 31st,
# will get billed on the 28th of every subsequent month, for the duration of the plan
# subscription was created. If the subscription was created on or before the 28th of the month,
# it gets billed on the same day, every month, for the duration of the plan. Subscriptions created on
# or between the 29th - 31st,
# will get billed on the 28th of every subsequent month, for the duration of the plan
# will get billed on the 28th of every subsequent month, for the duration of the plan

# TODO: REVISIT THIS
# MANUAL_RETRY, ETC
# The right place toupdate transaction_type for PaymentTransaction
