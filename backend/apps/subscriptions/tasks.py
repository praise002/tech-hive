import logging
from datetime import timedelta

from apps.subscriptions.choices import SubscriptionChoices
from apps.subscriptions.models import Subscription
from apps.subscriptions.services.notification_service import notification_service
from apps.subscriptions.services.subscription_service import subscription_service
from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,  # Gives access to 'self' (the task instance)
    max_retries=3,  # If the task itself crashes, retry it 3 times
    default_retry_delay=300,  # Wait 5 minutes before retrying crashed task
)
def retry_failed_payments(self):
    """
    Automatically retry failed subscription payments.

    Retry schedule:
    - Day 0: Initial failure
    - Day 3: First retry
    - Day 5: Second retry
    - Day 7: Third retry
    - Day 10: Grace period ends, subscription expires
    """
    try:
        now = timezone.now()

        logger.info("Starting automatic payment retry job...")

        # Find PAST_DUE subscriptions that need retry
        past_due_subscriptions = Subscription.objects.filter(
            status=SubscriptionChoices.PAST_DUE,
            retry_count__lt=3,  # Max 3 retries
            payment_failed_at__isnull=False,
        )

        retry_schedule = {
            0: 3,  # First retry on day 3
            1: 5,  # Second retry on day 5
            2: 7,  # Third retry on day 7
        }

        retries_attempted = 0
        retries_successful = 0
        retries_failed = 0

        for subscription in past_due_subscriptions:
            # Calculate days since payment failed
            days_since_failure = (now - subscription.payment_failed_at).days

            # Check if we should retry today
            expected_retry_day = retry_schedule.get(subscription.retry_count)

            if expected_retry_day and days_since_failure >= expected_retry_day:
                # Check if we already retried today
                if subscription.last_retry_at:
                    hours_since_last_retry = (
                        now - subscription.last_retry_at
                    ).total_seconds() / 3600
                    if hours_since_last_retry < 23:  # Wait 23 hours between retries
                        continue

                logger.info(
                    f"Retrying payment for {subscription.user.email} "
                    f"(Attempt #{subscription.retry_count + 1})"
                )

                # Attempt retry
                success, message, _ = subscription_service.retry_payment(
                    subscription=subscription,
                )

                retries_attempted += 1

                if success:
                    retries_successful += 1
                    logger.info(f"✓ Retry successful for {subscription.user.email}")
                else:
                    retries_failed += 1
                    logger.warning(
                        f"✗ Retry failed for {subscription.user.email}: {message}"
                    )

                try:
                    notification_service.send_retry_failed_email(
                        user=subscription.user,
                        subscription=subscription,
                        retry_number=subscription.retry_count,
                    )
                    logger.info(
                        f"Sent retry failed email to {subscription.user.email} "
                        f"(retry #{subscription.retry_count})"
                    )
                except Exception as e:
                    logger.error(f"Failed to send retry failed email: {str(e)}")

        logger.info(
            f"Retry job completed: {retries_attempted} attempted, "
            f"{retries_successful} successful, {retries_failed} failed"
        )

        return {
            "attempted": retries_attempted,
            "successful": retries_successful,
            "failed": retries_failed,
        }

    except Exception as exc:
        logger.error(f"Error in retry_failed_payments task: {str(exc)}")
        # Retry the task if it fails
        raise self.retry(exc=exc)


@shared_task
def expire_trials():
    """
    Expire trials that ended.
    Runs daily at midnight.
    """

    try:
        now = timezone.now()

        logger.info("Starting trial expiration job...")

        # Find trials that:
        # 1. Are still in TRIALING status
        # 2. Trial ended more than 24 hours ago
        expired_trials = Subscription.objects.filter(
            status=SubscriptionChoices.TRIALING,
            trial_end__lt=now - timedelta(hours=24),  # Ended >24h ago
            paystack_subscription_code__isnull=True,  # Never got Paystack code
        )

        expired_count = 0
        for subscription in expired_trials:
            subscription.expire()
            logger.info(f"Expired trial for {subscription.user.email}")
            expired_count += 1

        logger.info(f"Trial expiration completed: {expired_count} trials expired")

        return {"expired_count": expired_count}

    except Exception as exc:
        logger.error(f"Error in expire_unconverted_trials task: {str(exc)}")
        raise


@shared_task
def expire_grace_periods():
    """
    Expire subscriptions that exceeded grace period (10 days).
    Runs every 6 hours.
    """

    try:
        logger.info("Starting grace period expiration job...")

        # Find PAST_DUE subscriptions that exceeded grace period
        expired_grace_periods = Subscription.objects.grace_period_expired()

        expired_count = 0
        for subscription in expired_grace_periods:
            subscription_service.cancel_subscription(subscription)
            logger.info(
                f"Expired subscription for {subscription.user.email} "
                f"(grace period exceeded)"
            )
            expired_count += 1

        logger.info(f"Grace period expiration completed: {expired_count} expired")

        return {"expired_count": expired_count}

    except Exception as exc:
        logger.error(f"Error in expire_grace_periods task: {str(exc)}")
        raise


@shared_task
def send_trial_ending_reminders():
    """
    Send reminder emails to users whose trial is ending soon.
    Runs daily at 10 AM.
    """

    try:
        now = timezone.now()

        logger.info("Starting trial reminder job...")

        # Find trials ending in 2 days
        trials_ending_soon = Subscription.objects.trial_ending_soon()

        reminders_sent = 0
        for subscription in trials_ending_soon:
            days_remaining = (subscription.trial_end - now).days

            try:
                notification_service.send_trial_ending_reminder(
                    user=subscription.user,
                    subscription=subscription,
                    days_remaining=days_remaining,
                )
                logger.info(
                    f"Sent trial reminder to {subscription.user.email} "
                    f"({days_remaining} days remaining)"
                )
                reminders_sent += 1
            except Exception as e:
                logger.error(
                    f"Failed to send trial reminder to {subscription.user.email}: {str(e)}"
                )

        logger.info(f"Trial reminder job completed: {reminders_sent} reminders sent")

        return {"reminders_sent": reminders_sent}

    except Exception as exc:
        logger.error(f"Error in send_trial_ending_reminders task: {str(exc)}")
        raise


@shared_task
def send_upcoming_charge_reminders():
    """
    Send email 3 days before subscription renewal.
    Runs daily.
    """
    try:
        now = timezone.now()
        reminder_date = now + timedelta(days=3)

        logger.info("Starting upcoming charge reminder job...")

        # Find subscriptions renewing in 3 days
        upcoming_renewals = Subscription.objects.filter(
            status=SubscriptionChoices.ACTIVE,
            next_billing_date__date=reminder_date.date(),
        )

        reminders_sent = 0
        for subscription in upcoming_renewals:
            try:
                notification_service.send_upcoming_charge_email(
                    user=subscription.user,
                    subscription=subscription,
                    amount=subscription.plan.price,
                    charge_date=subscription.next_billing_date,
                )
                logger.info(
                    f"Sent upcoming charge reminder to {subscription.user.email}"
                )
                reminders_sent += 1
            except Exception as e:
                logger.error(
                    f"Failed to send upcoming charge email to {subscription.user.email}: {str(e)}"
                )

        logger.info(f"Upcoming charge reminders sent: {reminders_sent}")
        return {"reminders_sent": reminders_sent}

    except Exception as exc:
        logger.error(f"Error in send_upcoming_charge_reminders task: {str(exc)}")
        raise


@shared_task
def send_final_grace_warnings():
    """
    Send final warning email 1 day before grace period expires.
    Runs daily.
    """
    try:
        now = timezone.now()

        logger.info("Starting final grace period warning job...")

        # Find subscriptions expiring tomorrow
        expiring_tomorrow = Subscription.objects.filter(
            status=SubscriptionChoices.PAST_DUE,
            payment_failed_at__lte=now - timedelta(days=9),  # 9 days since failure
            payment_failed_at__gt=now - timedelta(days=10),  # Not yet 10 days
        )

        warnings_sent = 0
        for subscription in expiring_tomorrow:
            try:
                notification_service.send_final_grace_period_email(
                    user=subscription.user, subscription=subscription
                )
                logger.info(f"Sent final grace warning to {subscription.user.email}")
                warnings_sent += 1
            except Exception as e:
                logger.error(
                    f"Failed to send final grace warning to {subscription.user.email}: {str(e)}"
                )

        logger.info(f"Final grace warnings sent: {warnings_sent}")
        return {"warnings_sent": warnings_sent}

    except Exception as exc:
        logger.error(f"Error in send_final_grace_warnings task: {str(exc)}")
        raise
