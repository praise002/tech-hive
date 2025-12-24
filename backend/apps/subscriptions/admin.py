from django.contrib import admin
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from .models import PaymentTransaction, Subscription, SubscriptionPlan, WebhookLog


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "price_display",
        "billing_cycle",
        "paystack_plan_code",
        "is_active",
        "subscription_count",
    ]
    list_filter = ["is_active", "billing_cycle"]
    search_fields = ["name", "paystack_plan_code"]
    readonly_fields = ["id", "created_at", "updated_at"]
    # so it shows in admin interface and it shows below everything else

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "description", "price", "billing_cycle", "is_active")},
        ),
        ("Paystack Integration", {"fields": ("paystack_plan_code",)}),
        (
            "Features",
            {"fields": ("features",), "description": "Define premium features as JSON"},
        ),
        (
            "Metadata",
            {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def price_display(self, obj):
        return f"₦{obj.price:,.2f}"

    price_display.short_description = "Price"

    def subscription_count(self, obj):
        count = obj.subscriptions.filter(status__in=["TRIALING", "ACTIVE"]).count()
        return f"{count} active"

    subscription_count.short_description = "Subscriptions"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user_email",
        "plan_name",
        "status_badge",
        "trial_status",
        "next_billing_date",
        "days_remaining",
        "created_at",
    ]
    list_filter = ["status", "plan", "auto_renew", "cancel_at_period_end", "created_at"]
    search_fields = [
        "user__email",
        "user__first_name",
        "user__last_name",
        "paystack_subscription_code",
        "paystack_customer_code",
    ]
    readonly_fields = [
        "id",
        "created_at",
        "updated_at",
        "is_trial",
        "is_active",
        "days_until_expiry",
        "is_in_grace_period",
        "grace_period_ends_at",
    ]

    fieldsets = (
        ("User & Plan", {"fields": ("user", "plan", "status")}),
        (
            "Paystack Details",
            {
                "fields": (
                    "paystack_subscription_code",
                    "paystack_customer_code",
                    "paystack_authorization_code",
                )
            },
        ),
        ("Card Information", {"fields": ("card_last4", "card_type", "card_bank")}),
        (
            "Dates",
            {
                "fields": (
                    "start_date",
                    "trial_start",
                    "trial_end",
                    "current_period_start",
                    "current_period_end",
                    "next_billing_date",
                    "cancelled_at",
                    "expires_at",
                )
            },
        ),
        ("Billing Control", {"fields": ("auto_renew", "cancel_at_period_end")}),
        (
            "Payment Failure Tracking",
            {"fields": ("payment_failed_at", "retry_count", "last_retry_at")},
        ),
        ("Cancellation", {"fields": ("cancel_reason",), "classes": ("collapse",)}),
        (
            "Computed Properties",
            {
                "fields": (
                    "is_trial",
                    "is_active",
                    "days_until_expiry",
                    "is_in_grace_period",
                    "grace_period_ends_at",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Metadata",
            {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def user_email(self, obj):
        # namespace:appname_modelname_change(view, edit, change)
        url = reverse("admin:accounts_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)

    user_email.short_description = "User"

    def plan_name(self, obj):
        return obj.plan.name

    plan_name.short_description = "Plan"

    def status_badge(self, obj):
        colors = {
            "TRIALING": "#17a2b8",  # Blue
            "ACTIVE": "#28a745",  # Green
            "PAST_DUE": "#ffc107",  # Yellow
            "EXPIRED": "#6c757d",  # Gray
            "CANCELLED": "#dc3545",  # Red
        }
        color = colors.get(obj.status, "#6c757d")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = "Status"

    def trial_status(self, obj):
        if obj.is_trial:
            days_left = (obj.trial_end - timezone.now()).days
            return format_html(
                '<span style="color: #17a2b8;">✓ {} days left</span>', days_left
            )
        return "-"

    trial_status.short_description = "Trial"

    def days_remaining(self, obj):
        if obj.is_active:
            return f"{obj.days_until_expiry} days"
        return "-"

    days_remaining.short_description = "Days Left"

    # actions = ["mark_as_expired", "cancel_subscriptions"]
    

    # def mark_as_expired(self, request, queryset):
    #     count = 0
    #     for subscription in queryset:
    #         subscription.expire()
    #         count += 1
    #     self.message_user(request, f"{count} subscription(s) marked as expired.")

    # mark_as_expired.short_description = "Mark selected as expired"

    # def cancel_subscriptions(self, request, queryset):
    #     count = 0
    #     for subscription in queryset:
    #         if subscription.status in ["TRIALING", "ACTIVE"]:
    #             subscription.cancel(reason="Cancelled by admin")
    #             count += 1
    #     self.message_user(request, f"{count} subscription(s) cancelled.")

    # cancel_subscriptions.short_description = "Cancel selected subscriptions"


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = [
        "reference",
        "user_email",
        "amount_display",
        "status_badge",
        "transaction_type",
        "initiated_at",
    ]
    list_filter = ["status", "transaction_type", "is_retry", "initiated_at"]
    search_fields = ["reference", "paystack_reference", "user__email"]
    readonly_fields = [
        "id",
        "initiated_at",
        "created_at",
        "updated_at",
        "amount_in_kobo",
    ]

    fieldsets = (
        (
            "Transaction Details",
            {
                "fields": (
                    "user",
                    "subscription",
                    "reference",
                    "paystack_reference",
                    "amount",
                    "amount_in_kobo",
                    "currency",
                    "status",
                    "transaction_type",
                )
            },
        ),
        ("Timestamps", {"fields": ("initiated_at", "paid_at", "failed_at")}),
        (
            "Retry Information",
            {"fields": ("is_retry", "retry_number", "failure_reason")},
        ),
        ("Raw Response", {"fields": ("paystack_response",), "classes": ("collapse",)}),
        (
            "Metadata",
            {"fields": ("id", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "User"

    def amount_display(self, obj):
        return f"₦{obj.amount:,.2f}"

    amount_display.short_description = "Amount"

    def status_badge(self, obj):
        colors = {
            "PENDING": "#ffc107",
            "SUCCESS": "#28a745",
            "FAILED": "#dc3545",
            "ABANDONED": "#6c757d",
        }
        color = colors.get(obj.status, "#6c757d")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_badge.short_description = "Status"


@admin.register(WebhookLog)
class WebhookLogAdmin(admin.ModelAdmin):
    list_display = ["event_type", "processed_badge", "created_at", "processed_at"]
    list_filter = ["processed", "event_type", "created_at"]
    search_fields = ["event_type", "payload"]
    readonly_fields = ["id", "created_at", "payload", "signature"]

    fieldsets = (
        ("Webhook Details", {"fields": ("event_type", "signature")}),
        ("Payload", {"fields": ("payload",)}),
        ("Processing", {"fields": ("processed", "processed_at", "error")}),
        ("Metadata", {"fields": ("id", "created_at"), "classes": ("collapse",)}),
    )

    def processed_badge(self, obj):
        if obj.processed:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">✓ Processed</span>'
            )
        return format_html(
            '<span style="color: #ffc107; font-weight: bold;">⏳ Pending</span>'
        )

    processed_badge.short_description = "Status"

    actions = ["mark_as_unprocessed"]

    def mark_as_unprocessed(self, request, queryset):
        count = queryset.update(processed=False, processed_at=None, error=None)
        self.message_user(request, f"{count} webhook(s) marked as unprocessed.")

    mark_as_unprocessed.short_description = "Mark as unprocessed (for retry)"
