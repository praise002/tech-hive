from decimal import Decimal

from apps.common.models import BaseModel
from apps.subscriptions.choices import (
    StatusChoices,
    SubscriptionChoices,
    TransactionTypeChoices,
)
from apps.subscriptions.manager import SubscriptionManager
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class SubscriptionPlan(BaseModel):
    BILLING_CYCLE_CHOICES = [
        ("MONTHLY", "Monthly"),
        ("YEARLY", "Yearly"),
    ]

    name = models.CharField(
        max_length=20, help_text="Plan name (e.g., 'Premium Monthly')"
    )
    description = models.TextField(blank=True, help_text="Plan description for display")
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text="Price in Naira (e.g., 5000.00)",
    )
    features = models.TextField()
    paystack_plan_code = models.CharField(max_length=50)
    billing_cycle = models.CharField(
        max_length=20, choices=BILLING_CYCLE_CHOICES, default="MONTHLY"
    )
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    @property
    def price_in_kobo(self):
        """Convert price to kobo for Paystack API"""
        return int(self.price * 100)

    def get_feature(self, feature_name, default=None):
        """Safely get a feature value"""
        return self.features.get(feature_name, default)

    class Meta:
        ordering = ["price"]

    def __str__(self):
        return f"{self.name} - ₦{self.price}/{self.billing_cycle}"


class Subscription(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscription",
        help_text="User who owns this subscription",
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,  # Don't allow deleting plans with active subscriptions
        related_name="subscriptions",
        help_text="The premium plan user is subscribed to",
    )
    status = models.CharField(
        max_length=20,
        choices=SubscriptionChoices.choices,
        default=SubscriptionChoices.TRAILING,
        help_text="Current subscription status",
    )

    reference = models.CharField(
        max_length=20,
        help_text="Custom reference",
    )

    # Paystack Integration Fields
    paystack_subscription_code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Subscription code from Paystack (e.g., SUB_abc123xyz)",
    )
    paystack_customer_code = models.CharField(
        max_length=50, help_text="Customer code from Paystack (e.g., CUS_abc123xyz)"
    )
    paystack_authorization_code = models.CharField(
        max_length=50,
        help_text="Authorization code for charging card (e.g., AUTH_abc123xyz)",
    )
    paystack_email_token = models.CharField(
        max_length=50,
        help_text="Token for managing subscription on Paystack (e.g., d7gofp6yppn3qz7)",
        null=True,
        blank=True,
    )

    # Card details (for display only)
    card_last4 = models.CharField(
        max_length=4,
        null=True,
        blank=True,
        help_text="Last 4 digits of card (e.g., '1234')",
    )
    card_type = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Card type (e.g., 'visa', 'mastercard')",
    )
    card_bank = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Issuing bank (e.g., 'Access Bank')",
    )

    # ===== Date Fields =====
    start_date = models.DateTimeField(
        null=True, blank=True, help_text="When subscription started"
    )
    # a subscription may not start immediately
    updated_at = models.DateTimeField(auto_now=True)

    # Trial dates
    trial_start = models.DateTimeField(
        null=True, blank=True, help_text="When trial period started"
    )
    trial_end = models.DateTimeField(
        null=True, blank=True, help_text="When trial period ends"
    )

    # Billing cycle dates
    current_period_start = models.DateTimeField(
        help_text="Start of current billing period"
    )
    current_period_end = models.DateTimeField(help_text="End of current billing period")
    next_billing_date = models.DateTimeField(
        null=True, blank=True, help_text="When next charge will happen"
    )

    # Cancellation dates
    cancelled_at = models.DateTimeField(
        null=True, blank=True, help_text="When user clicked cancel"
    )
    expires_at = models.DateTimeField(
        null=True, blank=True, help_text="When subscription actually expires"
    )

    # ===== Billing Control =====
    auto_renew = models.BooleanField(
        default=True, help_text="Should subscription auto-renew?"
    )
    cancel_at_period_end = models.BooleanField(
        default=False,
        help_text="Cancel when current period ends (deferred cancellation)",
    )

    # ===== Payment Failure Tracking =====
    payment_failed_at = models.DateTimeField(
        null=True, blank=True, help_text="When payment first failed"
    )
    retry_count = models.IntegerField(
        default=0, help_text="Number of automatic retry attempts made"
    )
    last_retry_at = models.DateTimeField(
        null=True, blank=True, help_text="When last retry attempt was made"
    )

    # ===== Metadata =====
    cancel_reason = models.TextField(
        null=True, blank=True, help_text="Why user cancelled (optional feedback)"
    )

    objects = SubscriptionManager()

    @property
    def is_trial(self):
        """Check if currently in trial period"""
        return (
            self.status == "TRIALING"
            and self.trial_end
            and self.trial_end > timezone.now()
        )

    @property
    def is_active(self):
        """Check if subscription provides premium access"""
        if self.status in ["TRIALING", "ACTIVE", "PAST_DUE"]:
            return True

        # CANCELLED but still within paid period
        if self.status == "CANCELLED" and self.current_period_end > timezone.now():
            return True

        return False

    @property
    def days_until_expiry(self):
        """Days remaining in current period"""
        if not self.current_period_end:
            return 0

        delta = self.current_period_end - timezone.now()
        return max(0, delta.days)

    @property
    def is_in_grace_period(self):
        """Check if in grace period after payment failure"""
        if self.status != "PAST_DUE" or not self.payment_failed_at:
            return False

        # Grace period = 10 days (7 retry days + 3 final grace)
        grace_period_end = self.payment_failed_at + timezone.timedelta(days=10)
        return timezone.now() < grace_period_end

    @property
    def grace_period_ends_at(self):
        """When grace period ends"""
        if not self.payment_failed_at:
            return None
        return self.payment_failed_at + timezone.timedelta(days=10)

    def mark_as_paid(self):
        """Mark subscription as paid (after successful payment)"""
        self.status = "ACTIVE"
        self.retry_count = 0
        self.payment_failed_at = None
        self.last_retry_at = None
        self.save()

    def mark_as_failed(self):
        """Mark payment as failed"""
        self.status = "PAST_DUE"
        if not self.payment_failed_at:
            self.payment_failed_at = timezone.now()
        self.save()

    def increment_retry_count(self):
        """Increment retry counter"""
        self.retry_count += 1
        self.last_retry_at = timezone.now()
        self.save()

    def cancel(self, reason=None):
        """Cancel subscription"""
        cancellable_statuses = [
            SubscriptionChoices.ACTIVE,
            SubscriptionChoices.TRIALING,
            SubscriptionChoices.PAST_DUE,
        ]

        if self.status not in cancellable_statuses:
            status_messages = {
                SubscriptionChoices.CANCELLED: "Subscription is already cancelled",
                SubscriptionChoices.EXPIRED: "Cannot cancel an expired subscription",
            }
            error_message = status_messages.get(
                self.status, f"Cannot cancel subscription with status: {self.status}"
            )
            raise ValueError(error_message)

        self.cancelled_at = timezone.now()
        self.cancel_reason = reason
        self.auto_renew = False

        # Deferred cancellation: Keep access until period ends
        self.status = SubscriptionChoices.CANCELLED
        self.cancel_at_period_end = True

        self.save()

    def expire(self):
        """Expire subscription (end of period or grace period)"""
        self.status = "EXPIRED"
        self.expires_at = timezone.now()
        self.auto_renew = False
        self.save()

    def reactivate(self):
        """Reactivate a cancelled subscription"""
        if self.status != "CANCELLED":
            raise ValueError("Can only reactivate cancelled subscriptions")

        if timezone.now() > self.current_period_end:
            raise ValueError(
                "Subscription period has ended. Must create new subscription."
            )

        self.status = "ACTIVE"
        self.cancelled_at = None
        self.cancel_at_period_end = False
        self.auto_renew = True
        self.save()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["paystack_subscription_code"]),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.plan.name} ({self.status})"


class PaymentTransaction(BaseModel):
    """
    Records every payment attempt (success or failure).
    Used for billing history and debugging.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payment_transactions",
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
    )

    updated_at = models.DateTimeField(auto_now=True)

    # Transaction details
    reference = models.CharField(
        max_length=100,
        unique=True,
        help_text="Our internal reference (e.g., TXN_abc123xyz)",
    )
    paystack_reference = models.CharField(
        max_length=100,
        unique=True,
        help_text="Paystack's transaction reference",
    )

    # Payment details
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Amount in Naira",
    )
    currency = models.CharField(max_length=3, default="NGN", help_text="Currency code")

    # Status
    status = models.CharField(
        max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionTypeChoices.choices,
        help_text="What triggered this transaction",
    )

    # Dates
    initiated_at = models.DateTimeField(
        auto_now_add=True, help_text="When transaction was initiated"
    )
    paid_at = models.DateTimeField(
        null=True, blank=True, help_text="When payment was successful"
    )
    failed_at = models.DateTimeField(
        null=True, blank=True, help_text="When payment failed"
    )

    # Metadata
    failure_reason = models.TextField(
        null=True, blank=True, help_text="Why payment failed (from Paystack)"
    )
    is_retry = models.BooleanField(default=False, help_text="Is this a retry attempt?")
    retry_number = models.IntegerField(
        null=True, blank=True, help_text="Which retry attempt (1, 2, 3)"
    )

    # Raw Paystack response (for debugging)
    paystack_response = models.JSONField(
        null=True, blank=True, help_text="Full response from Paystack API"
    )

    class Meta:
        indexes = [
            models.Index(fields=["reference"]),
            models.Index(fields=["paystack_reference"]),
        ]

    def __str__(self):
        return f"{self.user.email} - ₦{self.amount} ({self.status})"

    @property
    def amount_in_kobo(self):
        """Convert amount to kobo for Paystack"""
        if self.amount:
            return int(self.amount * 100)

    def mark_as_success(self, paystack_response=None):
        """Mark transaction as successful"""
        self.status = StatusChoices.SUCCESS
        self.paid_at = timezone.now()
        if paystack_response:
            self.paystack_response = paystack_response
        self.save()

    def mark_as_failed(self, reason=None, paystack_response=None):
        """Mark transaction as failed"""
        self.status = StatusChoices.FAILED
        self.failed_at = timezone.now()
        self.failure_reason = reason
        if paystack_response:
            self.paystack_response = paystack_response
        self.save()


class WebhookLog(BaseModel):
    """
    Logs all webhook calls from Paystack.
    Useful for debugging and ensuring idempotency.
    """

    # Webhook details
    event_type = models.CharField(
        max_length=100,
        help_text="Event type (e.g., 'subscription.create')",
    )
    payload = models.JSONField(
        null=True, blank=True, help_text="Full webhook payload from Paystack"
    )
    signature = models.CharField(
        max_length=255, help_text="Paystack signature for verification"
    )

    # Processing status
    processed = models.BooleanField(
        default=False, help_text="Has this webhook been processed?"
    )
    processed_at = models.DateTimeField(
        null=True, blank=True, help_text="When webhook was processed"
    )

    # Error tracking
    error = models.TextField(
        null=True, blank=True, help_text="Any errors during processing"
    )

    # Timestamp
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="When webhook was received"
    )

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["event_type"]),
            models.Index(fields=["processed"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        status = "✓ Processed" if self.processed else "⏳ Pending"
        return f"{self.event_type} - {status}"

    def mark_as_processed(self):
        """Mark webhook as processed"""
        self.processed = True
        self.processed_at = timezone.now()
        self.save()

    def mark_as_failed(self, error_message):
        """Mark webhook processing as failed"""
        self.error = error_message
        self.processed = False
        self.save()
        self.error = error_message
        self.processed = False
        self.save()
        self.error = error_message
        self.processed = False
        self.save()
