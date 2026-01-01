from django.contrib import admin

from apps.analytics.models import (
    ArticleAnalytics,
    ContentView,
    DailyMetrics,
    SessionMetrics,
    UserActivity,
)


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
    readonly_fields = ["id", "timestamp", "created_at"]
    date_hierarchy = "timestamp"


@admin.register(ContentView)
class ContentViewAdmin(admin.ModelAdmin):
    list_display = [
        "content_type",
        "content_id",
        "user",
        "session",
        "device_type",
        "duration_seconds",
        "timestamp",
    ]
    list_filter = ["content_type", "device_type", "timestamp"]
    search_fields = ["user__username", "user__email", "referrer"]
    readonly_fields = ["id", "timestamp"]
    date_hierarchy = "timestamp"


@admin.register(ArticleAnalytics)
class ArticleAnalyticsAdmin(admin.ModelAdmin):
    list_display = [
        "article",
        "total_views",
        "unique_visitors",
        "avg_read_time",
        "completion_rate",
        "engagement_rate",
        "last_updated",
    ]
    list_filter = ["last_updated"]
    search_fields = ["article__title", "article__slug"]
    readonly_fields = [
        "id",
        "engagement_rate",
        "last_updated",
        "created_at",
    ]
    fieldsets = (
        (
            "Article Information",
            {
                "fields": ("article",),
            },
        ),
        (
            "View Metrics",
            {
                "fields": ("total_views", "unique_visitors", "avg_read_time", "completion_rate"),
            },
        ),
        (
            "Engagement Metrics",
            {
                "fields": (
                    "shares_count",
                    "reactions_count",
                    "comments_count",
                    "saves_count",
                    "engagement_rate",
                ),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("last_updated", "created_at"),
            },
        ),
    )


@admin.register(DailyMetrics)
class DailyMetricsAdmin(admin.ModelAdmin):
    list_display = [
        "date",
        "registered_users_count",
        "visitors_count",
        "total_active_users",
        "bounce_rate",
        "avg_session_duration",
        "updated_at",
    ]
    list_filter = ["date"]
    readonly_fields = [
        "id",
        "updated_at",
        "created_at",
    ]
    date_hierarchy = "date"
    fieldsets = (
        (
            "Date Information",
            {
                "fields": ("date",),
            },
        ),
        (
            "User Metrics",
            {
                "fields": (
                    "registered_users_count",
                    "visitors_count",
                    "total_active_users",
                ),
            },
        ),
        (
            "Session Metrics",
            {
                "fields": ("bounce_rate", "avg_session_duration", "avg_load_speed"),
            },
        ),
        (
            "Device Breakdown",
            {
                "fields": ("mobile_count", "tablet_count", "desktop_count"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("updated_at", "created_at"),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        """Make date readonly when editing existing object"""
        if obj:
            return self.readonly_fields + ["date"]
        return self.readonly_fields