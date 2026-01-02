import uuid

from apps.analytics.choices import (
    ContentTypeChoices,
    DeviceTypeChoices,
    EventTypeChoices,
)
from apps.common.models import BaseModel
from apps.content.models import Article
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

User = get_user_model()


class SessionMetrics(models.Model):
    """Aggregated session data for bounce rate and duration calculations"""

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    session_id = models.CharField(
        max_length=255,
        unique=True,
        help_text="Client-generated unique identifier stored in sessionStorage",
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="sessions"
    )
    start_time = models.DateTimeField(
        default=timezone.now,  # Auto-set but overridable
        help_text="When the session started",
    )
    end_time = models.DateTimeField(
        null=True, blank=True, help_text="When the session ended"
    )
    page_count = models.PositiveIntegerField(
        default=0, help_text="Number of pages viewed in this session"
    )
    total_duration = models.PositiveIntegerField(
        default=0, help_text="Total session duration in seconds"
    )
    device_type = models.CharField(max_length=50, choices=DeviceTypeChoices.choices)
    is_bounce = models.BooleanField(
        default=False, help_text="True if user left after viewing only one page"
    )

    class Meta:
        ordering = ["-start_time"]
        indexes = [
            models.Index(fields=["session_id"]),
            models.Index(fields=["user", "start_time"]),
            models.Index(fields=["is_bounce"]),
        ]
        verbose_name_plural = "Session Metrics"

    def __str__(self):
        return f"Session {self.session_id} - {self.start_time}"


class UserActivity(BaseModel):
    """Raw activity events for tracking user interactions"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(
        SessionMetrics,
        on_delete=models.CASCADE,
        related_name="activities",
        null=True,
        blank=True,
    )
    # Many UserActivity records can belong to one User
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # If user is deleted, keep activity but set user=NULL
        null=True,  # Allows NULL (anonymous users)
        blank=True,  # Form validation allows empty
        related_name="activities",  # Access all activities via user.activities.all()
    )
    event_type = models.CharField(max_length=50, choices=EventTypeChoices.choices)
    page_url = models.URLField(max_length=500)
    referrer = models.URLField(max_length=500, null=True, blank=True)

    # Device Information
    device_type = models.CharField(
        max_length=50, choices=DeviceTypeChoices.choices, null=True, blank=True
    )
    browser = models.CharField(max_length=100, null=True, blank=True)
    browser_version = models.CharField(max_length=50, null=True, blank=True)
    os = models.CharField(max_length=100, null=True, blank=True)
    os_version = models.CharField(max_length=50, null=True, blank=True)
    screen_resolution = models.CharField(max_length=50, null=True, blank=True)

    duration_seconds = models.PositiveIntegerField(
        default=0, help_text="Duration of activity in seconds"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional event-specific data (scroll_depth, article_id, etc.)",
    )
    load_time_ms = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Page load time in milliseconds (measured on frontend)"
    )

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["session_id"]),
            models.Index(fields=["timestamp"]),
            models.Index(fields=["session_id", "timestamp"]),
            models.Index(fields=["user", "timestamp"]),
            models.Index(fields=["device_type", "timestamp"]),
            models.Index(fields=["event_type", "timestamp"]),
        ]
        verbose_name_plural = "User Activities"

    def __str__(self):
        user_info = self.user.username if self.user else "Anonymous"
        return f"{self.event_type} - {user_info} - {self.timestamp}"


class ContentView(models.Model):
    """Individual content view tracking for detailed analytics"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_type = models.CharField(max_length=50, choices=ContentTypeChoices.choices)
    content_id = models.CharField(
        help_text="UUID of the content being tracked (e.g., Article, Job, or Event ID)"
    )
    # TODO: MIGHT REMOVE LATER BECAUSE IT IS REDUNDANT
    # Generic Foreign Key for flexible content relationship
    content_type_model = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True
    )
    object_id = models.CharField(null=True, blank=True)
    content_object = GenericForeignKey("content_type_model", "object_id")

    session = models.ForeignKey(
        SessionMetrics,
        on_delete=models.CASCADE,
        related_name="content_views",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="content_views",
    )
    referrer = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        help_text="Source URL that led to this page (e.g., 'https://google.com/search', 'https://twitter.com/post/123', 'https://techhive.com/home')",
    )
    device_type = models.CharField(max_length=50, choices=DeviceTypeChoices.choices)
    timestamp = models.DateTimeField(auto_now_add=True)
    duration_seconds = models.PositiveIntegerField(
        default=0, help_text="Time spent viewing content"
    )

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["content_type", "content_id", "timestamp"]),
            models.Index(fields=["user", "timestamp"]),
            models.Index(fields=["device_type", "timestamp"]),
            models.Index(fields=["session_id"]),
            models.Index(fields=["referrer"]),
        ]

    def __str__(self):
        return f"{self.content_type} {self.content_id} - {self.timestamp}"


# class ArticleAnalytics(BaseModel):
#     """Article-specific aggregated metrics"""

#     article = models.OneToOneField(
#         Article,
#         on_delete=models.CASCADE,
#         related_name="analytics",
#     )
#     total_views = models.PositiveIntegerField(default=0)
#     unique_visitors = models.PositiveIntegerField(
#         default=0,
#         help_text="Number of distinct users who viewed this article (counted once per user, regardless of multiple visits)",
#     )
#     avg_read_time = models.FloatField(
#         default=0.0, help_text="Average read time in minutes"
#     )
#     completion_rate = models.FloatField(
#         default=0.0,
#         validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
#         help_text="Percentage of users who completed reading",
#     )
#     shares_count = models.PositiveIntegerField(default=0)
#     reactions_count = models.PositiveIntegerField(default=0)
#     comments_count = models.PositiveIntegerField(default=0)
#     saves_count = models.PositiveIntegerField(default=0)

#     # Engagement rate calculation
#     engagement_rate = models.FloatField(
#         default=0.0, help_text="Calculated as (total_engagements / views) * 100"
#     )

#     last_updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ["-total_views"]
#         indexes = [
#             models.Index(fields=["article"]),  # Index on article_id
#             models.Index(fields=["total_views"]),
#             models.Index(fields=["last_updated"]),
#             models.Index(fields=["engagement_rate"]),
#         ]
#         verbose_name_plural = "Article Analytics"

#     def __str__(self):
#         return f"Analytics for {self.article.title}"

#     def calculate_engagement_rate(self):
#         """Calculate engagement rate based on formula"""
#         if self.total_views == 0:
#             return 0.0

#         total_engagements = (
#             self.shares_count
#             + self.reactions_count
#             + self.comments_count
#             + self.saves_count
#         )
#         return round((total_engagements / self.total_views) * 100, 1)

#     def save(self, *args, **kwargs):
#         """Auto-calculate engagement rate on save"""
#         self.engagement_rate = self.calculate_engagement_rate()
#         super().save(*args, **kwargs)


class DailyMetrics(BaseModel):
    """Pre-aggregated daily statistics for dashboard"""

    date = models.DateField(
        unique=True,
        help_text="Date for this metrics snapshot. Each date can only have one metrics record to prevent duplicate daily aggregations.",
    )
    registered_users_count = models.PositiveIntegerField(default=0)
    visitors_count = models.PositiveIntegerField(
        default=0, help_text="Anonymous visitors count"
    )
    total_active_users = models.PositiveIntegerField(default=0)

    bounce_rate = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Percentage of single-page sessions",
    )
    avg_session_duration = models.FloatField(
        default=0.0, help_text="Average session duration in minutes"
    )

    # Device breakdown
    mobile_count = models.PositiveIntegerField(default=0)
    tablet_count = models.PositiveIntegerField(default=0)
    desktop_count = models.PositiveIntegerField(default=0)

    # Performance metrics
    avg_load_speed = models.FloatField(
        default=0.0, help_text="Average page load speed in seconds"
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["date"]),
        ]
        verbose_name_plural = "Daily Metrics"

    def __str__(self):
        return f"Metrics for {self.date}"

    def calculate_device_percentages(self):
        """Calculate device type percentages"""
        total = self.mobile_count + self.tablet_count + self.desktop_count
        if total == 0:
            return {"mobile": 0, "tablet": 0, "desktop": 0}

        return {
            "mobile": round((self.mobile_count / total) * 100, 1),
            "tablet": round((self.tablet_count / total) * 100, 1),
            "desktop": round((self.desktop_count / total) * 100, 1),
        }
