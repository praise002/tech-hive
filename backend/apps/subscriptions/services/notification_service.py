import logging
from datetime import timezone
from decimal import Decimal

from apps.accounts.emails import EmailThread
from apps.subscriptions.models import PaymentTransaction, Subscription
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

User = get_user_model()
logger = logging.getLogger(__name__)


class NotificationService:
    """
    Handles all email notifications for subscriptions.
    """

    def __init__(self):
        self.frontend_url = settings.FRONTEND_URL

    def send_email(
        self, subject: str, recipient: str, template_name: str, context: dict
    ) -> bool:
        """
        Send email using Django email backend.

        Args:
            subject: Email subject
            recipient: Recipient email
            template_name: Template file name
            context: Template context

        Returns:
            True if sent successfully
        """
        context.update(
            {
                "frontend_url": self.frontend_url,
            }
        )
        message = render_to_string(template_name, context)
        email_message = EmailMessage(subject=subject, body=message, to=[recipient])
        email_message.content_subtype = "html"
        EmailThread(email_message).start()

    # ===== Trial Emails =====

    def send_trial_started_email(self, user, subscription: Subscription) -> bool:
        """Send email when trial starts."""
        context = {
            "user": user,
            "subscription": subscription,
            "trial_days": 7,
        }

        return self.send_email(
            subject="Welcome to Tech Hive Premium - Your 7-Day Trial Has Started!",
            recipient=user.email,
            template_name="trial_started.html",
            context=context,
        )

    def send_trial_ending_soon_email(
        self, user, subscription: Subscription, days_remaining
    ) -> bool:
        """Send email 2 days before trial ends."""

        context = {
            "user": user,
            "subscription": subscription,
            "days_remaining": days_remaining,
        }

        return self.send_email(
            subject=f"Your Tech Hive Premium Trial Ends in {days_remaining} Days",
            recipient=user.email,
            template_name="trial_ending_soon.html",
            context=context,
        )

    # ===== Payment Emails =====

    def send_payment_success_email(self, user, transaction: PaymentTransaction) -> bool:
        """Send email after successful payment."""
        context = {
            "user": user,
            "transaction": transaction,
            "subscription": transaction.subscription,
        }

        return self.send_email(
            subject="Payment Successful - Tech Hive Premium",
            recipient=user.email,
            template_name="payment_success.html",
            context=context,
        )

    def send_payment_failed_email(
        self, user, subscription: Subscription, reason: str
    ) -> bool:
        """Send email when payment fails."""
        context = {
            "user": user,
            "subscription": subscription,
            "failure_reason": reason,
            "retry_url": f"{self.frontend_url}/dashboard/subscription",
        }

        return self.send_email(
            subject="Payment Failed - Action Required",
            recipient=user.email,
            template_name="payment_failed.html",
            context=context,
        )

    def send_retry_scheduled_email(
        self, user, subscription: Subscription, next_retry_date
    ) -> bool:
        """Send email when retry is scheduled."""
        context = {
            "user": user,
            "subscription": subscription,
            "next_retry_date": next_retry_date,
        }

        return self.send_email(
            subject="Payment Retry Scheduled - Tech Hive Premium",
            recipient=user.email,
            template_name="retry_scheduled.html",
            context=context,
        )

    def send_retry_failed_email(
        self, user, subscription: Subscription, retry_number: int
    ) -> bool:
        """Send email when retry fails."""
        remaining_retries = 3 - retry_number

        context = {
            "user": user,
            "subscription": subscription,
            "retry_number": retry_number,
            "remaining_retries": remaining_retries,
        }

        return self.send_email(
            subject=f"Payment Retry #{retry_number} Failed",
            recipient=user.email,
            template_name="retry_failed.html",
            context=context,
        )

    def send_final_grace_period_email(self, user, subscription: Subscription) -> bool:
        """Send email during final grace period."""
        context = {
            "user": user,
            "subscription": subscription,
            "grace_period_ends": subscription.grace_period_ends_at,
        }

        return self.send_email(
            subject="Final Notice - Update Payment Method",
            recipient=user.email,
            template_name="final_grace_period.html",
            context=context,
        )

    def send_subscription_expired_email(self, user) -> bool:
        """Send email when subscription expires."""
        context = {
            "user": user,
            "resubscribe_url": f"{self.frontend_url}/pricing",
        }

        return self.send_email(
            subject="Your Tech Hive Premium Subscription Has Expired",
            recipient=user.email,
            template_name="subscription_expired.html",
            context=context,
        )

    def send_subscription_created_email(self, user, subscription: Subscription) -> bool:
        """
        Send email when a paid subscription is successfully created.
        """
        context = {
            "user": user,
            "subscription": subscription,
            "plan_name": subscription.plan.name,
            "amount": subscription.plan.price,
            "next_billing_date": subscription.next_billing_date,
        }

        return self.send_email(
            subject="Welcome to Tech Hive Premium!",
            recipient=user.email,
            template_name="subscription_created.html",
            context=context,
        )

    def send_upcoming_charge_email(
        self, user, subscription: Subscription, amount: Decimal, charge_date: str
    ) -> bool:
        """
        Send email 3 days before subscription renewal charge.
        """
        from django.utils.dateparse import parse_datetime

        # Parse the charge date if it's a string
        if isinstance(charge_date, str):
            charge_date_obj = parse_datetime(charge_date)
        else:
            charge_date_obj = charge_date

        context = {
            "user": user,
            "subscription": subscription,
            "amount": amount,
            "charge_date": charge_date_obj,
            "plan_name": subscription.plan.name,
            "card_last4": subscription.card_last4,
            "update_card_url": f"{self.frontend_url}/dashboard/subscription",
        }

        return self.send_email(
            subject="Upcoming Charge: Your Tech Hive Premium Renewal",
            recipient=user.email,
            template_name="upcoming_charge.html",
            context=context,
        )

    # ===== Cancellation Emails =====

    def send_cancellation_confirmed_email(
        self, user, subscription: Subscription
    ) -> bool:
        """Send email when subscription is cancelled."""
        context = {
            "user": user,
            "subscription": subscription,
            "access_until": subscription.current_period_end,
        }

        return self.send_email(
            subject="Subscription Cancelled - Tech Hive Premium",
            recipient=user.email,
            template_name="cancellation_confirmed.html",
            context=context,
        )

    def send_reactivation_email(self, user, subscription: Subscription) -> bool:
        """Send email when subscription is reactivated."""
        context = {
            "user": user,
            "subscription": subscription,
        }

        return self.send_email(
            subject="Welcome Back! Subscription Reactivated",
            recipient=user.email,
            template_name="reactivation_success.html",
            context=context,
        )

    # ===== Card Update Email =====

    def send_card_updated_email(self, user, subscription: Subscription) -> bool:
        """Send email when payment card is updated."""
        context = {
            "user": user,
            "subscription": subscription,
        }

        return self.send_email(
            subject="Payment Method Updated Successfully",
            recipient=user.email,
            template_name="card_updated.html",
            context=context,
        )

    def send_card_expiring_email(
        self, user, subscription: Subscription, expiry_date: str, card_description: str
    ) -> bool:
        """
        Send email when payment card is about to expire.
        """
        # Generate update link for the user to update their card
        from .paystack_service import paystack_service

        try:
            update_link = paystack_service.generate_update_subscription_link(
                subscription.paystack_subscription_code
            )
        except Exception as e:
            logger.error(f"Failed to generate update link for {user.email}: {str(e)}")
            update_link = f"{self.frontend_url}/dashboard/subscription"  # Fallback

        context = {
            "user": user,
            "subscription": subscription,
            "expiry_date": expiry_date,
            "card_description": card_description,
            "update_card_url": update_link,
        }

        return self.send_email(
            subject="Action Required: Your Payment Card is Expiring Soon",
            recipient=user.email,
            template_name="card_expiring.html",
            context=context,
        )


notification_service = NotificationService()
