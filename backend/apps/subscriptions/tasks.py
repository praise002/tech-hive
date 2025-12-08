from celery import shared_task
from django.utils import timezone
from apps.subscriptions.models import Subscription
from apps.subscriptions.choices import SubscriptionChoices
from apps.subscriptions.services.subscription_service import subscription_service
import logging

logger = logging.getLogger(__name__)


@shared_task(
    name='apps.subscriptions.tasks.retry_failed_payments',
    bind=True,
    max_retries=3,
    default_retry_delay=300,  # 5 minutes
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
                    is_manual=False,
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

        logger.info(
            f"Retry job completed: {retries_attempted} attempted, "
            f"{retries_successful} successful, {retries_failed} failed"
        )
        
        return {
            'attempted': retries_attempted,
            'successful': retries_successful,
            'failed': retries_failed,
        }

    except Exception as exc:
        logger.error(f"Error in retry_failed_payments task: {str(exc)}")
        # Retry the task if it fails
        raise self.retry(exc=exc)


@shared_task(name='apps.subscriptions.tasks.expire_unconverted_trials')
def expire_unconverted_trials():
    """
    Expire trials that ended but weren't converted to paid.
    Runs daily at midnight.
    """
    from datetime import timedelta
    
    try:
        now = timezone.now()
        
        logger.info("Starting trial expiration job...")
        
        # Find trials that:
        # 1. Are still in TRIALING status
        # 2. Trial ended more than 24 hours ago
        # 3. Haven't been paid
        unconverted_trials = Subscription.objects.filter(
            status=SubscriptionChoices.TRIALING,
            trial_end__lt=now - timedelta(hours=24),  # Ended >24h ago
            paystack_subscription_code__isnull=True,  # Never got Paystack code
        )
        
        expired_count = 0
        for subscription in unconverted_trials:
            subscription.expire()
            logger.info(f"Expired unconverted trial for {subscription.user.email}")
            expired_count += 1
        
        logger.info(f"Trial expiration completed: {expired_count} trials expired")
        
        return {'expired_count': expired_count}
        
    except Exception as exc:
        logger.error(f"Error in expire_unconverted_trials task: {str(exc)}")
        raise


@shared_task(name='apps.subscriptions.tasks.expire_grace_periods')
def expire_grace_periods():
    """
    Expire subscriptions that exceeded grace period (10 days).
    Runs every 6 hours.
    """
    from datetime import timedelta
    
    try:
        now = timezone.now()
        grace_period_days = 10
        
        logger.info("Starting grace period expiration job...")
        
        # Find PAST_DUE subscriptions that exceeded grace period
        expired_grace_periods = Subscription.objects.filter(
            status=SubscriptionChoices.PAST_DUE,
            payment_failed_at__lt=now - timedelta(days=grace_period_days),
        )
        
        expired_count = 0
        for subscription in expired_grace_periods:
            subscription.expire()
            logger.info(
                f"Expired subscription for {subscription.user.email} "
                f"(grace period exceeded)"
            )
            expired_count += 1
        
        logger.info(f"Grace period expiration completed: {expired_count} expired")
        
        return {'expired_count': expired_count}
        
    except Exception as exc:
        logger.error(f"Error in expire_grace_periods task: {str(exc)}")
        raise


@shared_task(name='apps.subscriptions.tasks.send_trial_ending_reminders')
def send_trial_ending_reminders():
    """
    Send reminder emails to users whose trial is ending soon.
    Runs daily at 10 AM.
    """
    from datetime import timedelta
    from apps.subscriptions.services.notification_service import notification_service
    
    try:
        now = timezone.now()
        
        logger.info("Starting trial reminder job...")
        
        # Find trials ending in 2 days
        trials_ending_soon = Subscription.objects.filter(
            status=SubscriptionChoices.TRIALING,
            trial_end__gte=now + timedelta(days=1),
            trial_end__lte=now + timedelta(days=3),
        )
        
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
        
        return {'reminders_sent': reminders_sent}
        
    except Exception as exc:
        logger.error(f"Error in send_trial_ending_reminders task: {str(exc)}")
        raise