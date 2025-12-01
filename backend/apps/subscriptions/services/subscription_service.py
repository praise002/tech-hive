import logging
import uuid
from datetime import timedelta
from decimal import Decimal
from typing import Dict, Optional, Tuple

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

    def create_subscription(
        self, user, plan: SubscriptionPlan, has_trial: bool = True
    ) -> Tuple[Subscription, PaymentTransaction, str]:
        """
        Initialize a new subscription for a user.

        Args:
            user: User subscribing
            plan: SubscriptionPlan to subscribe to
            has_trial: Whether to include 7-day trial

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
            amount = Decimal("0.00") if has_trial else plan.price

            # Calculate dates
            now = timezone.now()

            if has_trial:
                trial_start = now
                trial_end = now + timedelta(days=7)
                period_start = now
                period_end = trial_end
                next_billing = trial_end
                start_date = now
            else:
                period_start = None
                period_end = None
                next_billing = None

            # Prepare metadata
            metadata = {
                "user_id": str(user.id),
                "user_email": user.email,
                "plan_id": str(plan.id),
                "plan_name": plan.name,
                "has_trial": has_trial,
            }

            with transaction.atomic():
                # Create Subscription record
                subscription = Subscription.objects.create(
                    user=user,
                    plan=plan,
                    status="TRIALING" if has_trial else "ACTIVE",
                    start_date=now,
                    trial_start=trial_start,
                    trial_end=trial_end,
                    current_period_start=period_start,
                    current_period_end=period_end,
                    next_billing_date=next_billing,
                )

                # Initialize Paystack transaction
                if not has_trial:
                    paystack_response = paystack_service.initialize_transaction(
                        email=user.email,
                        amount=amount,
                        plan_code=plan.paystack_plan_code,
                        callback_url=f"{self._get_frontend_url()}/payment/callback",
                        metadata=metadata,
                        reference=reference,
                    )
                else:
                    # No Paystack initialization for trial subscriptions
                    paystack_response = {"reference": None}

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
