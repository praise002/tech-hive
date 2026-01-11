from apps.accounts.models import ContributorOnboarding, Otp, User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

admin.site.site_header = mark_safe(
    '<strong style="font-weight: bold;">TECH HIVE ADMIN </strong>'
)


class UserAdmin(BaseUserAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "is_email_verified",
        "is_active",
        "is_suspended",
        "created_at",
    )
    list_filter = (
        "is_email_verified",
        "is_active",
        "is_suspended",
        "is_staff",
        "is_superuser",
        "created_at",
    )
    ordering = ("first_name", "last_name", "email")
    list_per_page = 10

    fieldsets = (
        (_("Login Credentials"), {"fields": ("email", "password")}),
        (
            _("Personal Information"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "id",
                    "google_id",
                    "avatar",
                )
            },
        ),
        (
            _("User Preferences"),
            {
                "fields": (
                    "cursor_color",
                    "mentions_disabled",
                )
            },
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_email_verified",
                    "is_active",
                    "is_suspended",
                    "suspension_reason",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Important Dates"),
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "last_login",
                    "suspended_at",
                    "suspended_by",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "id",
                    "google_id",
                    "first_name",
                    "last_name",
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "is_suspended",
                    "avatar",
                    "cursor_color",
                    "mentions_disabled",
                ),
            },
        ),
    )

    readonly_fields = (
        "created_at",
        "username",
        "updated_at",
        "id",
        "google_id",
        "suspended_at",
        "suspended_by",
    )
    search_fields = ("first_name", "last_name", "email", "username")


admin.site.register(Otp)
admin.site.register(User, UserAdmin)


@admin.register(ContributorOnboarding)
class ContributorOnboardingAdmin(admin.ModelAdmin):
    list_display = ["id", "user_email", "terms_accepted", "accepted_at"]
    search_fields = ["user__email", "user__first_name", "user__last_name"]
    readonly_fields = ["id"]

    def user_email(self, obj):
        url = reverse("admin:accounts_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)

    user_email.short_description = "User"
