from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import PaymentTransaction, Subscription, SubscriptionPlan


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """
    Used to display available plans to the user.
    """

    class Meta:
        model = SubscriptionPlan
        fields = [
            "id",
            "name",
            "description",
            "price",
            "billing_cycle",
            "features",
        ]


class PaymentTransactionSerializer(serializers.ModelSerializer):
    """
    Used for the user's billing history.
    """

    class Meta:
        model = PaymentTransaction
        fields = [
            "id",
            "reference",
            "amount",
            "status",
            "transaction_type",
            "initiated_at",
            "paid_at",
            "failed_at",
            "failure_reason",
        ]


class SubscriptionDetailSerializer(serializers.ModelSerializer):
    """
    A detailed, read-only serializer for the Subscription model.
    This provides a comprehensive view of the user's subscription status.
    It uses SerializerMethodField to include data from model properties.
    """

    # Use the plan serializer to nest plan details
    plan = SubscriptionPlanSerializer(read_only=True)

    is_premium = serializers.BooleanField(source="is_active")
    is_trial = serializers.BooleanField()
    days_remaining = serializers.IntegerField(source="days_until_expiry")
    is_in_grace_period = serializers.BooleanField()
    grace_period_ends_at = serializers.DateTimeField()

    # A nested dictionary for card details
    card_details = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = [
            "id",
            "status",
            "plan",
            "is_premium",
            "is_trial",
            "trial_start",
            "trial_end",
            "current_period_start",
            "current_period_end",
            "next_billing_date",
            "days_remaining",
            "cancelled_at",
            "cancel_at_period_end",
            "is_in_grace_period",
            "grace_period_ends_at",
            "card_details",
        ]

    @extend_schema_field(serializers.DictField)
    def get_card_details(self, obj):
        """
        Groups card information into a nested object.
        Returns None if no card is on file.
        """
        if obj.card_last4:
            return {
                "last4": obj.card_last4,
                "type": obj.card_type,
                "bank": obj.card_bank,
            }
        return None


class SubscribeRequestSerializer(serializers.Serializer):
    """Serializer for subscribe request"""

    plan_id = serializers.UUIDField(required=True)
    start_trial = serializers.BooleanField(default=False)

    def validate_plan_id(self, value):
        """Validate plan exists and is active"""
        try:
            plan = SubscriptionPlan.objects.get(id=value, is_active=True)
            return plan
        except SubscriptionPlan.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive plan")


class CancelSubscriptionSerializer(serializers.Serializer):
    """
    Write-only serializer for cancelling a subscription.
    Includes an optional reason for cancellation.
    """

    reason = serializers.CharField(
        required=False, allow_blank=True, max_length=500, write_only=True
    )
