import logging
from decimal import Decimal
from typing import Dict

from apps.subscriptions.models import Subscription, WebhookLog
from django.db import transaction

from backend.apps.subscriptions.choices import (
    SubscriptionChoices,
    TransactionTypeChoices,
)
from backend.apps.subscriptions.services import notification_service

from .paystack_service import paystack_service
from .subscription_service import subscription_service

logger = logging.getLogger(__name__)


class WebhookService:
    """
    Processes Paystack webhook events.
    """

    def process_webhook(
        self, event_type: str, payload: Dict, signature: str, raw_body: bytes
    ) -> bool:
        """
        Main webhook processing entry point.

        Args:
            event_type: Type of event (e.g., 'charge.success')
            payload: Webhook payload
            signature: Paystack signature
            raw_body: Raw request body for signature verification

        Returns:
            True if processed successfully
        """
        try:
            # Verify signature
            if not paystack_service.verify_webhook_signature(raw_body, signature):
                logger.error("Invalid webhook signature")
                return False

            # Log webhook
            webhook_log = WebhookLog.objects.create(
                event_type=event_type,
                payload=payload,
                signature=signature,
            )

            try:
                # Route to appropriate handler
                handler_map = {
                    # happens on first subscription
                    "subscription.create": self.handle_subscription_create,
                    "charge.success": self.handle_charge_success,  # occurs if plan code used
                    # happens for each subsequent billing cycle
                    "invoice.create": self.handle_invoice_create,
                    "invoice.update": self.handle_invoice_update,
                    "subscription.not_renew": self.handle_subscription_not_renew,
                    "subscription.disable": self.handle_subscription_disable,
                    "invoice.payment_failed": self.handle_invoice_payment_failed,
                }

                handler = handler_map.get(event_type)

                if handler:
                    logger.info(f"Processing webhook: {event_type}")
                    handler(payload.get("data", {}))
                    webhook_log.mark_as_processed()
                    logger.info(f"Webhook processed successfully: {event_type}")
                else:
                    logger.warning(f"No handler for webhook event: {event_type}")
                    webhook_log.mark_as_processed()  # Mark as processed to avoid retry

                return True

            except Exception as e:
                error_message = f"Error processing webhook: {str(e)}"
                logger.error(error_message)
                webhook_log.mark_as_failed(error_message)
                raise

        except Exception as e:
            logger.error(f"Webhook processing failed: {str(e)}")
            return False

    def handle_subscription_create(self, data: Dict) -> None:
        """
        Handle subscription.create event.
        Fired when user authorizes card for subscription.
        A subscription.create event is sent to indicate that a subscription was
        created for the customer who was charged.
        """
        try:
            subscription_code = data.get("subscription_code")
            customer = data.get("customer", {})
            authorization = data.get("authorization", {})

            customer_code = customer.get("customer_code")
            customer_email = customer.get("email")

            # Find subscription by user email
            subscription = (
                Subscription.objects.filter(
                    user__email=customer_email, paystack_subscription_code__isnull=True
                )
                .order_by("-created_at")
                .first()
            )

            try:
                notification_service.send_subscription_created_email(
                    user=subscription.user,
                    subscription=subscription,
                )
                logger.info(f"Sent subscription created email to {customer_email}")
            except Exception as e:
                logger.error(
                    f"Failed to send subscription created email to {customer_email}: {str(e)}"
                )

            if not subscription:
                logger.warning(f"No subscription found for email: {customer_email}")
                return

            # Update subscription with Paystack data
            with transaction.atomic():
                # NOTE: the actual endpoint returns email token but webhook doesn't
                subscription.paystack_subscription_code = subscription_code
                subscription.paystack_customer_code = customer_code
                subscription.paystack_authorization_code = authorization.get(
                    "authorization_code"
                )
                subscription.card_last4 = authorization.get("last4")
                subscription.card_type = authorization.get("card_type")
                subscription.card_bank = authorization.get("bank")
                subscription.save()

                logger.info(
                    f"Subscription created: {subscription_code} for {customer_email}"
                )

        except Exception as e:
            logger.error(f"Error handling subscription.create: {str(e)}")
            raise

    def handle_charge_success(self, data: Dict) -> None:
        """
        Handle charge.success event.

        Sent when a charge is successful.
        For subscriptions, invoice.update will follow with complete info.

        First time payment & recurring payment

        Key difference from invoice.update:
        - charge.success: Immediate success notification, basic info
        - invoice.update: Complete invoice + subscription context

        Data structure:
        {
            "reference": "qTPrJoy9Bx",
            "status": "success",
            "amount": 10000,
            "gateway_response": "Approved by Financial Institution",
            "paid_at": "2016-09-30T21:10:19.000Z",
            "customer": {
                "customer_code": "CUS_xxx",
                "email": "user@example.com"
            },
            "authorization": {
                "authorization_code": "AUTH_xxx",
                "last4": "8877",
                "card_type": "mastercard DEBIT",
                "bank": "Guaranty Trust Bank"
            },
            "plan": {},  // Usually empty for subscription charges
            "metadata": {}
        }
        """
        try:
            customer = data.get("customer", {})
            customer_code = customer.get("customer_code")
            metadata = customer.get("metadata")
            amount = Decimal(data.get("amount", 0)) / Decimal(
                ("100")
            )  # Convert from kobo

            authorization = data.get("authorization", {})
            card_last4 = authorization.get("last4")

            # Find subscription by customer code
            subscription = None

            if customer_code:
                subscription = Subscription.objects.filter(
                    paystack_customer_code=customer_code
                ).first()

            if not subscription:
                logger.warning(f"No subscription found for charge: {customer_code}")
                return

            # Process as successful payment
            # First subscription
            if metadata is None:
                payment_transaction = subscription_service.process_successful_payment(
                    subscription=subscription,
                    transaction_data=data,
                    transaction_type=TransactionTypeChoices.SUBSCRIPTION,
                )
            else:
                # on next payment
                payment_transaction = subscription_service.process_successful_payment(
                    subscription=subscription,
                    transaction_data=data,
                    transaction_type=TransactionTypeChoices.RENEWAL,
                )
                # TODO: RETRY, MANUAL RETRY, REACTIVATION

            logger.info(
                f"Charge successful for {subscription.user.email}: ₦{amount}, Card: ****{card_last4}"
            )

            try:
                notification_service.send_payment_success_email(
                    user=subscription.user,
                    transaction=payment_transaction,
                )
                logger.info(f"Sent payment success email to {subscription.user.email}")
            except Exception as e:
                logger.error(
                    f"Failed to send payment success email to {subscription.user.email}: {str(e)}"
                )

        except Exception as e:
            logger.error(f"Error handling charge.success: {str(e)}")
            raise

    def handle_invoice_create(self, data: Dict) -> None:
        """
        Handle invoice.create event.

        Sent 3 days before next payment date as advance notice.
        Used to notify customers of upcoming charges.

        Flow:
        1. invoice.create (3 days before) ← WE ARE HERE
        2. charge.success/invoice.payment_failed (on billing date)
        3. invoice.update (after charge attempt)

        Data structure:
        {
            "invoice_code": "INV_xxx",
            "amount": 50000,
            "status": "pending",  // or "success" if retroactive
            "paid": false,  // Usually false at creation
            "period_start": "2018-12-20T15:00:00.000Z",
            "period_end": "2019-01-19T23:59:59.000Z",
            "subscription": {
                "subscription_code": "SUB_xxx",
                "status": "active",
                "next_payment_date": "2018-12-20T00:00:00.000Z"
            },
            "customer": {
                "email": "user@example.com",
                "customer_code": "CUS_xxx"
            }
        }
        """
        try:
            invoice_code = data.get("invoice_code")
            invoice_status = data.get("status")
            paid = data.get("paid", False)
            amount = Decimal(data.get("amount", 0)) / Decimal("100")

            # Get subscription info
            subscription_data = data.get("subscription", {})
            subscription_code = subscription_data.get("subscription_code")
            next_payment_date = subscription_data.get("next_payment_date")

            # Get customer info
            customer_data = data.get("customer", {})
            customer_email = customer_data.get("email")

            logger.info(
                f"Invoice created: {invoice_code} - "
                f"Amount: ₦{amount}, Status: {invoice_status}, Paid: {paid}"
            )

            # Find subscription
            subscription = None

            if subscription_code:
                subscription = Subscription.objects.filter(
                    paystack_subscription_code=subscription_code
                ).first()

            if not subscription:
                logger.warning(
                    f"No subscription found for invoice: {invoice_code} "
                    f"(sub: {subscription_code}, email: {customer_email})"
                )
                return

            # Check if this is advance notice (unpaid) or retroactive (paid)
            if not paid and invoice_status == "pending":
                # This is advance notice - 3 days before charge
                logger.info(
                    f"Upcoming charge notification for {subscription.user.email}: "
                    f"₦{amount} on {next_payment_date}"
                )

                try:
                    notification_service.send_upcoming_charge_email(
                        user=subscription.user,
                        subscription=subscription,
                        amount=amount,
                        charge_date=next_payment_date,
                    )
                    logger.info(
                        f"Sent upcoming charge email to {subscription.user.email}"
                    )
                except Exception as e:
                    logger.error(
                        f"Failed to send upcoming charge email to {subscription.user.email}: {str(e)}"
                    )

            elif paid and invoice_status == "success":
                # This is retroactive invoice creation (payment already happened)
                logger.info(
                    f"Retroactive invoice created (already paid): {subscription.user.email}"
                )

                # invoice.update will handle the actual payment processing
                # We just log this for now

            else:
                # Other status - just log
                logger.info(
                    f"Invoice created with status '{invoice_status}' for {subscription.user.email}"
                )

        except Exception as e:
            logger.error(f"Error handling invoice.create: {str(e)}")
            raise

    def handle_invoice_update(self, data: Dict) -> None:
        """
        Handle invoice.update event.

        Fired after a charge attempt as the final confirmation.
        Used to reconcile our DB state with Paystack's final invoice status.
        """
        try:
            invoice_code = data.get("invoice_code")
            subscription_data = data.get("subscription", {})
            subscription_code = subscription_data.get("subscription_code")
            customer_data = data.get("customer", {})
            customer_code = customer_data.get("customer_code")
            customer_email = customer_data.get("email")

            # Find the subscription using multiple strategies
            subscription = None
            if subscription_code:
                subscription = Subscription.objects.filter(
                    paystack_subscription_code=subscription_code
                ).first()
            if not subscription and customer_code:
                subscription = Subscription.objects.filter(
                    paystack_customer_code=customer_code
                ).first()
            if not subscription and customer_email:
                subscription = (
                    Subscription.objects.filter(user__email=customer_email)
                    .order_by("-created_at")
                    .first()
                )

            if not subscription:
                logger.warning(
                    f"[invoice.update] No subscription found for invoice {invoice_code}. "
                    f"Sub Code: {subscription_code}, Cust Code: {customer_code}"
                )
                return

            # If the user updaates their card via the paystack management link
            new_auth_data = data.get("authorization")
            new_auth_data = data.get("authorization")
            if new_auth_data:
                new_auth_code = new_auth_data.get("authorization_code")
                # Check if the authorization code is new or different
                if (
                    new_auth_code
                    and new_auth_code != subscription.paystack_authorization_code
                ):
                    logger.info(
                        f"[invoice.update] New payment method detected for {subscription.user.email}. "
                        f"Updating from ...{subscription.card_last4} to ...{new_auth_data.get('last4')}."
                    )
                    subscription.paystack_authorization_code = new_auth_code
                    subscription.card_last4 = new_auth_data.get("last4")
                    subscription.card_type = new_auth_data.get("card_type")
                    subscription.card_bank = new_auth_data.get("bank")
                    # Save these specific fields
                    #
                    subscription.save(
                        update_fields=[
                            "paystack_authorization_code",
                            "card_last4",
                            "card_type",
                            "card_bank",
                        ]
                    )

            # Analyze the final status of the invoice
            invoice_status = data.get("status")
            is_paid = data.get("paid", False)

            logger.info(
                f"[invoice.update] Received for {subscription.user.email}. "
                f"Invoice: {invoice_code}, Status: {invoice_status}, Paid: {is_paid}"
            )

            # --- Main Reconciliation Logic ---
            if invoice_status == "success" and is_paid:
                # Update the billing periods from paystack
                period_start = data.get("period_start")
                period_end = data.get("period_end")
                subscription_data = data.get("subscription", {})
                next_payment_date = subscription_data.get("next_payment_date")
                subscription_service.process_successful_payment(
                    period_start=period_start,
                    period_end=period_end,
                    next_billing_date=next_payment_date,
                )

                # SCENARIO A: Payment was successful.
                # Verify our system agrees.
                if subscription.status != SubscriptionChoices.ACTIVE:
                    logger.warning(
                        f"[invoice.update] State mismatch for {subscription.user.email}. "
                        f"DB status is '{subscription.status}', but invoice is paid. Correcting."
                    )
                    # This will set status to ACTIVE, update billing dates, and reset retries.
                    subscription_service.process_successful_payment(
                        subscription=subscription,
                        transaction_data=data.get("transaction", data),
                        transaction_type=TransactionTypeChoices.RENEWAL,
                        period_start=period_start,
                        period_end=period_end,
                        next_billing_date=next_payment_date,
                    )
                else:
                    logger.info(
                        f"[invoice.update] Successfully confirmed paid status for {subscription.user.email}."
                    )

            elif invoice_status in ["failed", "pending"] and not is_paid:
                # SCENARIO B: Payment failed.
                # Verify our system agrees.
                if subscription.status != SubscriptionChoices.PAST_DUE:
                    logger.warning(
                        f"[invoice.update] State mismatch for {subscription.user.email}. "
                        f"DB status is '{subscription.status}', but invoice is unpaid. Correcting."
                    )
                    # This will set status to PAST_DUE and start the grace period.
                    failure_reason = "Payment failed per invoice update"
                    subscription_service.process_failed_payment(
                        subscription=subscription,
                        failure_reason=failure_reason,
                        transaction_data=data,
                    )
                else:
                    logger.info(
                        f"[invoice.update] Successfully confirmed unpaid status for {subscription.user.email}."
                    )

        except Exception as e:
            logger.error(f"Error handling invoice.update: {str(e)}")
            raise

    def handle_invoice_payment_failed(self, data: Dict) -> None:
        """
        Handle invoice.payment_failed event.

        Sent when subscription charge attempt fails.
        Invoice remains open (unpaid), subscription stays active in Paystack.
        WE need to manage PAST_DUE state and grace period.

        Key Points:
        - Invoice status: "pending" (not "failed")
        - Subscription status: "active" (Paystack doesn't auto-disable)
        - transaction: {} (empty - no charge made)
        - open_invoice: Contains the unpaid invoice code

        What happens:
        1. Mark our subscription as PAST_DUE
        2. Record failure
        3. Start retry schedule (Day 3, 5, 7)
        4. Send failure notification
        5. User keeps premium access during grace period

        Data structure:
        {
            "invoice_code": "INV_xxx",
            "status": "pending",
            "paid": false,
            "paid_at": null,
            "transaction": {},  // Empty - no transaction
            "subscription": {
                "status": "active",  // Still active!
                "subscription_code": "SUB_xxx",
                "open_invoice": "INV_xxx",  // Unpaid invoice
                "next_payment_date": "2019-03-25T00:00:00.000Z"
            },
            "customer": {
                "email": "user@example.com",
                "customer_code": "CUS_xxx"
            },
            "authorization": {
                "authorization_code": "AUTH_xxx",
                "last4": "6666"
            }
        }
        """
        try:
            invoice_code = data.get("invoice_code")
            amount = Decimal(data.get("amount", 0)) / Decimal("100")

            # Get subscription info
            subscription_data = data.get("subscription", {})
            subscription_code = subscription_data.get("subscription_code")
            open_invoice = subscription_data.get("open_invoice")
            # paystack_subscription_status = subscription_data.get("status")

            # Get customer info
            customer_data = data.get("customer", {})
            customer_email = customer_data.get("email")

            # Get authorization (card that failed)
            authorization_data = data.get("authorization", {})
            card_last4 = authorization_data.get("last4")

            logger.warning(
                f"Invoice payment failed: {invoice_code} - "
                f"Amount: ₦{amount}, Customer: {customer_email}, "
                f"Card: ****{card_last4}, Open Invoice: {open_invoice}"
            )

            # Find subscription by subscription_code
            subscription = None

            if subscription_code:
                subscription = Subscription.objects.filter(
                    paystack_subscription_code=subscription_code
                ).first()

            if not subscription:
                logger.warning(
                    f"No subscription found for invoice: {invoice_code}. "
                    f"Subscription code: {subscription_code}"
                )
                return

            # Important: Check if already PAST_DUE (avoid duplicate processing)
            if (
                subscription.status == SubscriptionChoices.PAST_DUE
                and subscription.payment_failed_at
            ):
                logger.info(
                    f"Subscription already marked as PAST_DUE: {subscription.user.email}. "
                    f"Skipping duplicate processing."
                )
                return

            # Process failed payment
            reason = "Invoice payment failed"
            subscription_service.process_failed_payment(
                subscription=subscription,
                failure_reason=reason,
                transaction_data=data,
            )

            logger.warning(
                f"Invoice payment failed for {subscription.user.email}. "
                f"Invoice: {invoice_code}, Amount: ₦{amount}"
            )

            notification_service.send_payment_failed_email(
                user=subscription.user, reason=reason
            )

        except Exception as e:
            logger.error(f"Error handling invoice.payment_failed: {str(e)}")
            raise

    def handle_subscription_not_renew(self, data: Dict) -> None:
        """
        Handle subscription.not_renew event.

        Fired immediately after a subscription is set to not renew (i.e., cancelled).
        This is a confirmation webhook, not a trigger for cancellation.

        Our action:
        1. Find the subscription by its code.
        2. Verify that our local status is already 'CANCELLED'.
        3. If not, log a warning and correct the state.
        """
        try:
            subscription_code = data.get("subscription_code")
            paystack_status = data.get("status")  # Should be 'non-renewing'
            customer_email = data.get("customer", {}).get("email")

            logger.info(
                f"[subscription.not_renew] Received for {customer_email}. "
                f"Paystack status: {paystack_status}"
            )

            # 1. Find the subscription
            subscription = Subscription.objects.filter(
                paystack_subscription_code=subscription_code
            ).first()

            if not subscription:
                logger.warning(
                    f"[subscription.not_renew] No subscription found for code: {subscription_code}"
                )
                return

            # 2. Reconcile State: Check if our DB matches Paystack's intent
            if subscription.status == SubscriptionChoices.CANCELLED:
                # This is the correct and expected state.
                logger.info(
                    f"[subscription.not_renew] Confirmed non-renewing status for already "
                    f"cancelled subscription: {subscription.user.email}"
                )
            else:
                # This is a state mismatch. Our system thinks the subscription is still
                # active, but Paystack knows it's been cancelled.
                logger.warning(
                    f"[subscription.not_renew] State mismatch for {subscription.user.email}. "
                    f"DB status is '{subscription.status}', but Paystack status is 'non-renewing'. "
                    f"Correcting by cancelling locally."
                )
                # Correct our local state to match Paystack's reality.
                subscription.cancel(reason="Cancellation confirmed via webhook.")

        except Exception as e:
            logger.error(f"Error handling subscription.not_renew: {str(e)}")
            raise

    def handle_subscription_disable(self, data: Dict) -> None:
        """
        Handle subscription.disable event.

        Fired on the next payment date for a cancelled subscription, confirming
        it is now fully expired and access should be removed.

        Our action:
        1. Find the subscription.
        2. Change its status from 'CANCELLED' to 'EXPIRED'.
        """
        try:
            subscription_code = data.get("subscription_code")
            paystack_status = data.get("status")  #  'complete'
            customer_email = data.get("customer", {}).get("email")

            logger.info(
                f"[subscription.disable] Received for {customer_email}. "
                f"Paystack status: {paystack_status}"
            )

            # 1. Find the subscription
            subscription = Subscription.objects.filter(
                paystack_subscription_code=subscription_code
            ).first()

            if not subscription:
                logger.warning(
                    f"[subscription.disable] No subscription found for code: {subscription_code}"
                )
                return

            # 2. Expire the subscription
            if subscription.status != SubscriptionChoices.EXPIRED:
                logger.info(
                    f"Expiring subscription for {subscription.user.email} as its period has ended."
                )
                subscription.expire()
            else:
                logger.info(
                    f"Confirmed expired status for already expired subscription: {subscription.user.email}"
                )

        except Exception as e:
            logger.error(f"Error handling subscription.disable: {str(e)}")
            raise

    def handle_subscription_expiring_cards(self, data: list) -> None:
        """
        Handle subscription.expiring_cards event.

        Sent at the beginning of each month with info about subscriptions whose cards will expire soon.
        Used to notify customers to update their payment method.

        Data structure:
        {
        "expiry_date": "12/2021",
        "description": "visa ending with 4081",
        "brand": "visa",
        "subscription": { ... },
        "customer": { ... }
        }
        """
        try:
            for entry in data:
                expiry_date = entry.get("expiry_date")
                description = entry.get("description")
                subscription_info = entry.get("subscription", {})
                customer_info = entry.get("customer", {})

                subscription_code = subscription_info.get("subscription_code")
                customer_email = customer_info.get("email")

                # Find subscription
                subscription = Subscription.objects.filter(
                    paystack_subscription_code=subscription_code
                ).first()

                if not subscription:
                    logger.warning(
                        f"[expiring_cards] No subscription found for code: {subscription_code} ({customer_email})"
                    )
                    continue

                # Log the expiring card
                logger.info(
                    f"[expiring_cards] Card expiring soon for {customer_email}: {description} (expires {expiry_date})"
                )

                # Send notification email to customer
                try:
                    notification_service.send_card_expiring_email(
                        user=subscription.user,
                        subscription=subscription,
                        expiry_date=expiry_date,
                        card_description=description,
                    )
                    logger.info(f"Sent card expiring email to {customer_email}")
                except Exception as e:
                    logger.error(
                        f"Failed to send card expiring email to {customer_email}: {str(e)}"
                    )

        except Exception as e:
            logger.error(f"Error handling subscription.expiring_cards: {str(e)}")
            raise


webhook_service = WebhookService()


#
