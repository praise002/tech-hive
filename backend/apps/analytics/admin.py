from apps.analytics.models import SessionMetrics, UserActivity
from django.contrib import admin


@admin.register(SessionMetrics)
class SessionMetricsAdmin(admin.ModelAdmin):
    list_display = [
        "session_id",
        "user",
        "start_time",
        "end_time",
        "page_count",
        "total_duration",
        "device_type",
        "is_bounce",
    ]
    list_filter = ["device_type", "is_bounce", "start_time"]
    search_fields = ["user__username", "user__email"]
    readonly_fields = ["id", "session_id"]
    date_hierarchy = "start_time"


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = [
        "event_type",
        "user",
        "session",
        "page_url",
        "device_type",
        "duration_seconds",
        "timestamp",
    ]
    list_filter = ["event_type", "device_type", "timestamp"]
    search_fields = ["user__username", "user__email", "page_url", "session__session_id"]
    readonly_fields = ["id", "timestamp"]
    date_hierarchy = "timestamp"
