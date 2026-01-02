import logging
from datetime import timedelta

from apps.analytics.models import (
    ArticleAnalytics,
    DailyMetrics,
    SessionMetrics,
    UserActivity,
)
from apps.content.models import Article
from django.db.models import Avg, Count, F, Q, Sum
from django.utils import timezone

from backend.apps.analytics.choices import EventTypeChoices

logger = logging.getLogger(__name__)


class AnalyticsService:
    """
    Service for calculating analytics metrics
    """

    @staticmethod
    def get_date_range(period="weekly"):
        """
        Get start and end dates for the specified period
        """
        end_date = timezone.now().date()

        if period == "weekly":
            # Last 7 days including today
            start_date = end_date - timedelta(days=6)
            previous_start = start_date - timedelta(days=6)
        elif period == "monthly":
            start_date = end_date - timedelta(days=30)
            previous_start = start_date - timedelta(days=29)
        else:
            start_date = end_date - timedelta(days=6)
            previous_start = start_date - timedelta(days=6)

        return {
            "current_start": start_date,
            "current_end": end_date,
            "previous_start": previous_start,
            "previous_end": start_date,
        }

    @staticmethod
    def calculate_metric_with_trend(current_value, previous_value):
        """
        Calculate percentage change and trend direction

        Args:
            current_value: Metric from current period (e.g., this week)
            previous_value: Metric from previous period (e.g., last week)

        Returns:
            Dict with change percentage, trend direction, and previous value
        """
        if previous_value == 0:
            change_percentage = 0
        else:
            change_percentage = (
                (current_value - previous_value) / previous_value
            ) * 100

        return {
            "change_percentage": round(abs(change_percentage), 2),
            "trend": "down" if change_percentage < 0 else "up",
        }

    @classmethod
    def calculate_time_on_page(cls, period="weekly"):
        """
        Calculate average time users spend on pages
        Returns time in minutes
        """
        date_range = cls.get_date_range(period)

        # Current period - average session duration in seconds
        current_avg = (
            UserActivity.objects.filter(
                timestamp__gte=date_range["current_start"],
                timestamp__lte=date_range["current_end"],
                duration_seconds__isnull=False,
                duration_seconds__gt=0,  # Exclude zero/invalid durations
            ).aggregate(avg_duration=Avg("duration_seconds"))["avg_duration"]
            or 0
        )

        # Previous period
        previous_avg = (
            UserActivity.objects.filter(
                timestamp__gte=date_range["previous_start"],
                timestamp__lt=date_range["previous_end"],
                duration_seconds__isnull=False,
                duration_seconds__gt=0,
            ).aggregate(avg_duration=Avg("duration_seconds"))["avg_duration"]
            or 0
        )

        current_minutes = current_avg / 60
        previous_minutes = previous_avg / 60

        trend_data = cls.calculate_metric_with_trend(current_minutes, previous_minutes)

        return {"value": round(current_minutes, 1), "unit": "minutes", **trend_data}

    @classmethod
    def calculate_bounce_rate(cls, period="weekly"):
        """
        Calculate bounce rate (sessions with only 1 page view)
        Returns percentage
        """
        date_range = cls.get_date_range(period)

        # Current period
        current_total = SessionMetrics.objects.filter(
            start_time__gte=date_range["current_start"],
            start_time__lte=date_range["current_end"],
        ).count()

        current_bounces = SessionMetrics.objects.filter(
            start_time__gte=date_range["current_start"],
            start_time__lte=date_range["current_end"],
            is_bounce=True,
        ).count()

        # Previous period
        previous_total = SessionMetrics.objects.filter(
            start_time__gte=date_range["previous_start"],
            start_time__lt=date_range["previous_end"],
        ).count()

        previous_bounces = SessionMetrics.objects.filter(
            start_time__gte=date_range["previous_start"],
            start_time__lt=date_range["previous_end"],
            is_bounce=True,
        ).count()

        current_rate = (
            (current_bounces / current_total * 100) if current_total > 0 else 0
        )
        previous_rate = (
            (previous_bounces / previous_total * 100) if previous_total > 0 else 0
        )

        trend_data = cls.calculate_metric_with_trend(current_rate, previous_rate)

        return {"value": round(current_rate, 0), "unit": "percentage", **trend_data}

    @classmethod
    def calculate_load_speed(cls, period="weekly"):
        """
        Calculate average page load speed
        Returns time in seconds
        """
        date_range = cls.get_date_range(period)

        # Current period - average load time in milliseconds
        current_avg_ms = (
            UserActivity.objects.filter(
                event_type=EventTypeChoices.PAGE_LOAD,
                timestamp__gte=date_range["current_start"],
                timestamp__lte=date_range["current_end"],
                load_time_ms__isnull=False,
                load_time_ms__gt=0,
            ).aggregate(avg_load=Avg("load_time_ms"))["avg_load"]
            or 0
        )

        # Previous period
        previous_avg_ms = (
            UserActivity.objects.filter(
                event_type="page_load",
                timestamp__gte=date_range["previous_start"],
                timestamp__lt=date_range["previous_end"],
                load_time_ms__isnull=False,
                load_time_ms__gt=0,
            ).aggregate(avg_load=Avg("load_time_ms"))["avg_load"]
            or 0
        )

        # 1 second = 1,000 milliseconds
        current_seconds = current_avg_ms / 1000
        previous_seconds = previous_avg_ms / 1000

        trend_data = cls.calculate_metric_with_trend(current_seconds, previous_seconds)

        return {"value": round(current_seconds, 1), "unit": "seconds", **trend_data}

    @classmethod
    def get_device_distribution(cls, period="weekly"):
        """
        Get distribution of device types (Mobile, Tablet, Desktop)
        """
        date_range = cls.get_date_range(period)

        device_counts = (
            UserActivity.objects.filter(
                timestamp__gte=date_range["current_start"],
                timestamp__lte=date_range["current_end"],
            )
            .values("device_type")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        total = sum(item["count"] for item in device_counts)

        result = []
        for item in device_counts:
            device_type = item["device_type"] or "Unknown"
            count = item["count"]
            percentage = (count / total * 100) if total > 0 else 0

            result.append(
                {
                    "name": device_type,
                    "value": count,
                    "percentage": round(percentage, 0),
                }
            )

        return result

    @classmethod
    def get_active_users_timeline(cls, period="weekly"):
        """
        Get daily breakdown of active users (registered vs visitors)
        """
        date_range = cls.get_date_range(period)
        current_date = date_range["current_start"].date()
        end_date = date_range["current_end"].date()

        expected_days = (
            end_date - current_date
        ).days + 1  # +1 to include both endpoints

        # Use DailyMetrics if available, otherwise calculate from UserActivity
        daily_data = DailyMetrics.objects.filter(
            date__gte=current_date,
            date__lte=end_date,
        ).order_by("date")

        if daily_data.count() == expected_days:
            result = []
            for day in daily_data:
                result.append(
                    {
                        "date": day.date.isoformat(),
                        # Abbreviated weekday name e.g "Mon"
                        "day": day.date.strftime("%a"),
                        "registered_users": day.registered_users_count,
                        "visitors": day.visitors_count,
                        "total_active_users": day.total_active_users,
                    }
                )
            return result

        # Fallback: Calculate from UserActivity
        result = []

        while current_date <= end_date:
            next_date = current_date + timedelta(days=1)

            registered = (
                UserActivity.objects.filter(
                    timestamp__date=current_date, user__isnull=False
                )
                .values("user")
                .distinct()
                .count()
            )

            visitors = (
                UserActivity.objects.filter(
                    timestamp__date=current_date, user__isnull=True
                )
                .values("session")
                .distinct()
                .count()
            )

            result.append(
                {
                    "date": current_date.isoformat(),
                    "day": current_date.strftime("%a"),
                    "registered_users": registered,
                    "visitors": visitors,
                    "total_active_users": registered + visitors,
                }
            )

            current_date = next_date

        return result

    @classmethod
    def get_dashboard_metrics(cls, period="weekly"):
        """
        Get all dashboard metrics in a single call
        """
        date_range = cls.get_date_range(period)

        return {
            "period": period,
            "date_range": {
                "start": date_range["current_start"].isoformat(),
                "end": date_range["current_end"].isoformat(),
            },
            "metrics": {
                "time_on_page": cls.calculate_time_on_page(period),
                "bounce_rate": cls.calculate_bounce_rate(period),
                "load_speed": cls.calculate_load_speed(period),
            },
            "device_types": cls.get_device_distribution(period),
            "active_users": cls.get_active_users_timeline(period),
            "top_performing_posts": cls.get_top_performing_posts(period),
        }
