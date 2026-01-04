import uuid

from apps.analytics.choices import DeviceTypeChoices, EventTypeChoices
from apps.common.models import BaseModel
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class SessionMetrics(models.Model):
    """
    Aggregated session data for bounce rate and duration calculations
    For bounce rate, time on page
    """

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
    """
    Raw activity events for tracking user interactions
    All tracked by frontend
    """

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
    page_url = models.URLField(
    max_length=500,
    help_text="Full URL of the page where the activity occurred (e.g., 'https://techhive.com/articles/intro-to-react')"
)
    referrer = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        help_text="Source URL that led to this page (e.g., 'https://google.com/search', 'https://twitter.com/post/123', 'https://techhive.com/home')",
    )

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
        help_text="Additional event-specific data (job_id, article_id, etc.)",
    )
    load_time_ms = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Page load time in milliseconds (measured on frontend)",
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
