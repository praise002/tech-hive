import logging
from decimal import Decimal
from typing import Dict

from apps.subscriptions.models import Subscription, WebhookLog
from django.db import transaction

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
                    "subscription.create": self.handle_subscription_create,
                    "charge.success": self.handle_charge_success,
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
        """
        try:
            subscription_code = data.get("subscription_code")
            email_token = data.get("email_token")
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

            if not subscription:
                logger.warning(f"No subscription found for email: {customer_email}")
                return

            # Update subscription with Paystack data
            with transaction.atomic():
                subscription.paystack_subscription_code = subscription_code
                subscription.paystack_customer_code = customer_code
                subscription.paystack_email_token = email_token
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
        Fired when payment is successful (on next payment).
        """
        try:
            reference = data.get("reference")
            customer = data.get("customer", {})
            customer_code = customer.get("customer_code")
            amount = Decimal(data.get("amount", 0)) / Decimal(
                ("100")
            )  # Convert from kobo

            # Find subscription by customer code or reference
            subscription = None

            if customer_code:
                subscription = Subscription.objects.filter(
                    paystack_customer_code=customer_code
                ).first()

            if not subscription:
                logger.warning(f"No subscription found for charge: {reference}")
                return

            # Process successful payment
            subscription_service.process_successful_payment(
                subscription=subscription,
                transaction_data=data,
                transaction_type="RENEWAL",
            )

            logger.info(f"Charge successful for {subscription.user.email}: ₦{amount}")

        except Exception as e:
            logger.error(f"Error handling charge.success: {str(e)}")
            raise

    def handle_subscription_not_renew(self, data: Dict) -> None:
        """
        Handle subscription.not_renew event.
        Fired when subscription renewal payment fails.
        """
        try:
            subscription_code = data.get("subscription_code")

            # Find subscription
            subscription = Subscription.objects.filter(
                paystack_subscription_code=subscription_code
            ).first()

            if not subscription:
                logger.warning(f"No subscription found: {subscription_code}")
                return

            # Process failed payment
            failure_reason = "Subscription renewal failed"
            subscription_service.process_failed_payment(
                subscription=subscription,
                failure_reason=failure_reason,
                transaction_data=data,
            )

            logger.warning(f"Subscription not renewed: {subscription.user.email}")

        except Exception as e:
            logger.error(f"Error handling subscription.not_renew: {str(e)}")
            raise

    def handle_invoice_payment_failed(self, data: Dict) -> None:
        """
        Handle invoice.payment_failed event.
        Fired when subscription invoice payment fails.
        """
        try:
            invoice_code = data.get("invoice_code")
            subscription_code = data.get("subscription_code")
            customer = data.get("customer", {})
            customer_code = customer.get("customer_code")
            gateway_response = data.get("gateway_response", "Invoice payment failed")
            amount = Decimal(data.get("amount", 0)) / Decimal("100")

            # Find subscription by subscription_code
            subscription = None

            if subscription_code:
                subscription = Subscription.objects.filter(
                    paystack_subscription_code=subscription_code
                ).first()

            # Fallback: try by customer_code
            if not subscription and customer_code:
                subscription = Subscription.objects.filter(
                    paystack_customer_code=customer_code
                ).first()

            if not subscription:
                logger.warning(
                    f"No subscription found for invoice: {invoice_code}. "
                    f"Subscription code: {subscription_code}"
                )
                return

            # Process failed payment
            subscription_service.process_failed_payment(
                subscription=subscription,
                failure_reason=f"Invoice payment failed: {gateway_response}",
                transaction_data=data,
            )

            logger.warning(
                f"Invoice payment failed for {subscription.user.email}. "
                f"Invoice: {invoice_code}, Amount: ₦{amount}, Reason: {gateway_response}"
            )

        except Exception as e:
            logger.error(f"Error handling invoice.payment_failed: {str(e)}")
            raise

    def handle_subscription_disable(self, data: Dict) -> None:
        """
        Handle subscription.disable event.
        Fired when subscription is disabled/cancelled.
        """
        try:
            subscription_code = data.get("subscription_code")

            # Find subscription
            subscription = Subscription.objects.filter(
                paystack_subscription_code=subscription_code
            ).first()

            if not subscription:
                logger.warning(f"No subscription found: {subscription_code}")
                return

            # Subscription already cancelled in our system via API
            # Just log for confirmation
            logger.info(f"Subscription disable confirmed: {subscription.user.email}")

        except Exception as e:
            logger.error(f"Error handling subscription.disable: {str(e)}")
            raise

    # def handle_invoice_update(self, data: Dict) -> None:
    #     """
    #     Handle invoice.update event.
    #     Fired after charge attempt (success or failure).

    #     This contains the final status of the invoice:
    #     - 'success': Payment succeeded
    #     - 'failed': Payment failed
    #     - 'pending': Still processing
    #     """
    #     try:
    #         subscription_code = data.get("subscription", {}).get("subscription_code")
    #         customer = data.get("customer", {})
    #         customer_email = customer.get("email")
    #         invoice_status = data.get("status")  # 'success', 'failed', 'pending'
    #         amount = Decimal(data.get("amount", 0)) / 100
    #         paid = data.get("paid", False)
    #         paid_at = data.get("paid_at")

    #         # Find subscription
    #         subscription = self._find_subscription_by_code_or_email(
    #             subscription_code=subscription_code, email=customer_email
    #         )
    #         if not subscription:
    #             logger.warning(
    #                 f"No subscription found for invoice.update: {subscription_code}"
    #             )
    #             return

    #         # Process based on invoice status
    #         if invoice_status == "success" and paid:
    #             # Payment successful - update subscription if not already done
    #             if subscription.status == "PAST_DUE":
    #                 # Recovery from failed payment
    #                 subscription_service.process_successful_payment(
    #                     subscription=subscription,
    #                     transaction_data=data,
    #                     transaction_type="RENEWAL",
    #                 )

    #                 logger.info(
    #                     f"Invoice paid (recovery): {subscription.user.email} - ₦{amount}"
    #                 )
    #             else:
    #                 logger.info(
    #                     f"Invoice paid (already processed): {subscription.user.email} - ₦{amount}"
    #                 )
    #         elif invoice_status == "failed" and not paid:
    #             # Payment failed - mark as past due if not already done
    #             if subscription.status != "PAST_DUE":
    #                 failure_reason = data.get(
    #                     "gateway_response", "Invoice payment failed"
    #                 )
    #                 subscription_service.process_failed_payment(
    #                     subscription=subscription,
    #                     failure_reason=failure_reason,
    #                     transaction_data=data,
    #                 )

    #                 logger.warning(
    #                     f"Invoice failed: {subscription.user.email} - {failure_reason}"
    #                 )
    #             else:
    #                 logger.info(
    #                     f"Invoice failed (already marked): {subscription.user.email}"
    #                 )

    #         elif invoice_status == "pending":
    #             # Payment still processing - just log it
    #             logger.info(f"Invoice pending for {subscription.user.email}: ₦{amount}")

    #         else:
    #             logger.warning(
    #                 f"Unknown invoice status: {invoice_status} for {subscription.user.email}"
    #             )
    #     except Exception as e:
    #         logger.error(f"Error handling invoice.update: {str(e)}")
    #         raise


webhook_service = WebhookService()


# TODO: UPDATE CARD DETAILS
