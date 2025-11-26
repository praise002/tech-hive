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
                    # happens on first subscription
                    "subscription.create": self.handle_subscription_create,
                    "charge.success": self.handle_charge_success,  # occurs if plan code used
                    # happens for each subsequent billing cycle
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
    
    # TODO:
    def handle_charge_success(self, data: Dict) -> None:
        """
        Handle charge.success event.
        If you created the subscription by adding a plan code to a transaction, 
        a charge.success event is also sent to indicate that the transaction was successful.
        """
        try:
            customer = data.get("customer", {})
            customer_code = customer.get("customer_code")
            amount = Decimal(data.get("amount", 0)) / Decimal(
                ("100")
            )  # Convert from kobo

            # Find subscription by customer code 
            subscription = None

            if customer_code:
                subscription = Subscription.objects.filter(
                    paystack_customer_code=customer_code
                ).first()

            if not subscription:
                logger.warning(f"No subscription found for charge: {customer_code}")
                return

            # Process successful payment
            subscription_service.process_successful_payment(
                subscription=subscription,
                transaction_data=data,
                transaction_type="SUBSCRIPTION",
            )

            logger.info(f"Charge successful for {subscription.user.email}: ₦{amount}")

        except Exception as e:
            logger.error(f"Error handling charge.success: {str(e)}")
            raise
    
    # TODO:
    def handle_subscription_not_renew(self, data: Dict) -> None:
        """
        Handle subscription.not_renew event.
        A subscription.not_renew event will be sent to indicate that the subscription will 
        not renew on the next payment date.
        """
        pass
    
    # TODO:
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
    
    # TODO:
    def handle_subscription_disable(self, data: Dict) -> None:
        """
        Handle subscription.disable event.
        Fired when subscription is disabled/cancelled.
        On the next payment date, a subscription.disable event will be sent to indicate that 
        the subscription has been cancelled.
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

    def handle_invoice_update(self, data: Dict) -> None:
        pass
    


webhook_service = WebhookService()


# TODO: UPDATE CARD DETAILS IMPLEMENTATION
