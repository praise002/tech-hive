from django.db import models
from django.utils import timezone


class SubscriptionManager(models.Manager):
    """Custom manager for Subscription model"""
    
    def get_active_subscription(self, user):
        """Get user's active subscription (if any)"""
        return self.filter(
            user=user,
            status__in=['TRIALING', 'ACTIVE', 'PAST_DUE', 'CANCELLED']
        ).first()

    def get_latest_subscription(self, user):
        """Get user's most recent subscription (active or expired)"""
        return self.filter(user=user).order_by('-created_at').first()

    def active(self):
        """Get all active subscriptions (including trials and grace period)"""
        return self.filter(status__in=["TRIALING", "ACTIVE", "PAST_DUE"])

    def expired(self):
        """Get all expired subscriptions"""
        return self.filter(status="EXPIRED")

    def past_due(self):
        """Get subscriptions with failed payments"""
        return self.filter(status="PAST_DUE")

    def in_trial(self):
        """Get subscriptions currently in trial"""
        now = timezone.now()
        return self.filter(status="TRIALING", trial_end__gt=now)

    def trial_ending_soon(self, days=2):
        """Get trials ending within specified days"""
        now = timezone.now()
        end_date = now + timezone.timedelta(days=days)
        return self.filter(status="TRIALING", trial_end__range=(now, end_date))

    def grace_period_expired(self):
        """Get subscriptions where grace period has ended"""
        # payment_failed_at + 10 days < now
        now = timezone.now()
        grace_period_cutoff = now - timezone.timedelta(days=10)
        return self.filter(
            status="PAST_DUE", payment_failed_at__lte=grace_period_cutoff
        )

    def cancelled_and_expired(self):
        """Get cancelled subscriptions where period has ended"""
        now = timezone.now()
        return self.filter(
            status="CANCELLED", cancel_at_period_end=True, current_period_end__lte=now
        )
