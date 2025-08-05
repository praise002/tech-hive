from apps.accounts.models import Otp, User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

admin.site.site_header = mark_safe(
    '<strong style="font-weight: bold;">TECH HIVE ADMIN </strong>'
)


class UserAdmin(BaseUserAdmin):
    list_display = ("first_name", "last_name", "is_email_verified", "created_at")
    list_filter = list_display
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
                    "role",
                )
            },
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_email_verified",
                    "is_active",
                    "user_active",
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
                    "is_deleted",
                    "deleted_at",
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
                    "user_active",
                    "avatar",
                    "role",
                ),
            },
        ),
    )

    readonly_fields = ("created_at", "username", "updated_at", "id", "google_id")
    search_fields = ("first_name", "last_name", "email")


admin.site.register(Otp)
admin.site.register(User, UserAdmin)
