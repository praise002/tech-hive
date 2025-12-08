from django.db import models


class SubscriptionChoices(models.TextChoices):
    TRIALING = "TRIALING", "Trialing"  # In free trial period
    ACTIVE = "ACTIVE", "Active"  # Paid and current
    PAST_DUE = "PAST_DUE", "Past Due"  # Payment failed, in grace period
    EXPIRED = "EXPIRED", "Expired"  # Subscription ended
    CANCELLED = "CANCELLED", "Cancelled"  # User cancelled, waiting for period end


class StatusChoices(models.TextChoices):
    PENDING = "PENDING", "Pending"
    SUCCESS = "SUCCESS", "Success"
    FAILED = "FAILED", "Failed"
    ABANDONED = "ABANDONED", "Abandoned"


class TransactionTypeChoices(models.TextChoices):
    SUBSCRIPTION = "SUBSCRIPTION", "New Subscription"
    RENEWAL = "RENEWAL", "Monthly Renewal"
