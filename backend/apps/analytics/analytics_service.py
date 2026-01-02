import logging
from datetime import timedelta
from typing import Any, Dict, List, Optional

from apps.analytics.models import (
    ArticleAnalytics,
    ContentView,
    SessionMetrics,
    UserActivity,
)
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Q
from django.db.models.functions import TruncDate
from django.utils import timezone

User = get_user_model()
logger = logging.getLogger(__name__)


class AnalyticsService:
    """
    Handles all analytics business logic and calculations.

    This service provides methods for:
    - Bounce rate calculations
    - Session duration analytics
    - Device distribution metrics
    - User activity trends
    - Content performance tracking
    """

    def calculate_bounce_rate(
        self,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> float:
        """
        Calculate the percentage of single-page sessions (bounce rate).

        Bounce rate is a key engagement metric. A "bounce" occurs when a user
        visits only one page and leaves without any interaction.

        Args:
            date_from: Start date (ISO format: "2024-01-01")
            date_to: End date (ISO format: "2024-01-31")

        Returns:
            float: Bounce rate percentage (0.0 to 100.0)

        Example:
            # Last 7 days bounce rate
            bounce_rate = analytics_service.calculate_bounce_rate(
                date_from='2024-01-01',
                date_to='2024-01-07'
            )
            # Returns: 45.5 (45.5% of sessions were bounces)
        """
        try:
            logger.info(
                f"Calculating bounce rate "
                f"(from: {date_from or 'beginning'}, to: {date_to or 'now'})"
            )

            queryset = SessionMetrics.objects.all()

            if date_from:
                # WHERE start_time >= '2024-01-01'
                queryset = queryset.filter(start_time__gte=date_from)
            if date_to:
                # WHERE start_time <= '2024-01-31'
                queryset = queryset.filter(start_time__lte=date_to)

            total_sessions = queryset.count()
            bounced_sessions = queryset.filter(is_bounce=True).count()

            if total_sessions == 0:
                logger.warning("No sessions found for bounce rate calculation")
                return 0.0

            bounce_rate = (bounced_sessions / total_sessions) * 100
            bounce_rate = round(bounce_rate, 2)

            logger.info(
                f"Bounce rate calculated: {bounce_rate}% "
                f"({bounced_sessions}/{total_sessions} sessions)"
            )

            return bounce_rate

        except Exception as e:
            logger.error(f"Error calculating bounce rate: {str(e)}")
            raise Exception(f"Failed to calculate bounce rate: {str(e)}")

    def calculate_avg_session_duration(
        self,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        return_format: str = "minutes",  # "minutes" or "seconds"
    ) -> float:
        """
        Calculate average time users spend on the site per session.

        Session duration indicates content stickiness and user engagement.
        Longer sessions typically mean more engaged users.

        Args:
            date_from: Start date (ISO format)
            date_to: End date (ISO format)
            return_format: "minutes" (default) or "seconds"

        Returns:
            float: Average session duration in requested format

        Example:
            # Get average session duration for last month
            avg_duration = analytics_service.calculate_avg_session_duration(
                date_from='2024-12-01',
                date_to='2024-12-31',
                return_format='minutes'
            )
            # Returns: 3.5 (3.5 minutes average)
        """
        try:
            logger.info(
                f"Calculating average session duration "
                f"(from: {date_from or 'beginning'}, to: {date_to or 'now'})"
            )

            queryset = SessionMetrics.objects.all()

            if date_from:
                queryset = queryset.filter(start_time__gte=date_from)
            if date_to:
                queryset = queryset.filter(start_time__lte=date_to)

            avg_duration = queryset.aggregate(avg_duration=Avg("total_duration"))[
                "avg_duration"
            ]

            if avg_duration is None:
                logger.warning("No sessions found for duration calculation")
                return 0.0

            if return_format == "minutes":
                avg_duration = avg_duration / 60
                unit = "minutes"
            else:
                unit = "seconds"

            avg_duration = round(avg_duration, 2)

            logger.info(f"Average session duration calculated: {avg_duration} {unit}")

            return avg_duration

        except Exception as e:
            logger.error(f"Error calculating average session duration: {str(e)}")
            raise Exception(f"Failed to calculate average session duration: {str(e)}")

    # TODO: HOW ABOUT MONTHLY
    def get_device_distribution(
        self,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> Dict[str, float]:
        """
        Get breakdown of traffic by device type (Mobile/Tablet/Desktop).

        Device distribution helps prioritize:
        - Responsive design efforts
        - Performance optimization targets
        - Ad targeting strategies

        Args:
            date_from: Start date (ISO format)
            date_to: End date (ISO format)

        Returns:
            Dict with device percentages:
            {
                'mobile': 65.0,    # 65% mobile traffic
                'tablet': 10.0,    # 10% tablet
                'desktop': 25.0,   # 25% desktop
                'total_sessions': 1000
            }

        Example:
            device_dist = analytics_service.get_device_distribution(
                date_from='2024-01-01'
            )
            print(f"Mobile: {device_dist['mobile']}%")
        """
        try:
            logger.info(
                f"Calculating device distribution "
                f"(from: {date_from or 'beginning'}, to: {date_to or 'now'})"
            )

            queryset = SessionMetrics.objects.all()

            if date_from:
                queryset = queryset.filter(start_time__gte=date_from)
            if date_to:
                queryset = queryset.filter(start_time__lte=date_to)

            total_sessions = queryset.count()

            if total_sessions == 0:
                logger.warning("No sessions found for device distribution")
                return {
                    "mobile": 0.0,
                    "tablet": 0.0,
                    "desktop": 0.0,
                    "total_sessions": 0,
                }

            device_counts = queryset.values("device_type").annotate(count=Count("id"))

            result = {
                "mobile": 0.0,
                "tablet": 0.0,
                "desktop": 0.0,
                "total_sessions": total_sessions,
            }

            for device in device_counts:
                device_type = device["device_type"].lower()
                count = device["count"]
                percentage = round((count / total_sessions) * 100, 2)

                if device_type in result:
                    result[device_type] = percentage

            logger.info(
                f"Device distribution calculated: "
                f"Mobile {result['mobile']}%, "
                f"Tablet {result['tablet']}%, "
                f"Desktop {result['desktop']}% "
                f"({total_sessions} total sessions)"
            )

            return result

        except Exception as e:
            logger.error(f"Error calculating device distribution: {str(e)}")
            raise Exception(f"Failed to calculate device distribution: {str(e)}")

    # TODO: HOW ABOUT MONTHLY
    def get_active_users_trend(
        self,
        days: int = 7,
        include_anonymous: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Track daily active user counts over time for trend analysis.

        This creates time-series data perfect for line charts showing
        growth trends, traffic spikes, or user retention patterns.

        Args:
            days: Number of days to look back (default: 7)
            include_anonymous: Count anonymous users (default: True)

        Returns:
            List of daily user counts:
            [
                {
                    'date': '2024-01-01',
                    'registered_users': 850,
                    'anonymous_users': 400,
                    'total_users': 1250
                },
                {
                    'date': '2024-01-02',
                    'registered_users': 920,
                    'anonymous_users': 460,
                    'total_users': 1380
                },
                ...
            ]

        Example:
            # Get last 30 days trend
            trend = analytics_service.get_active_users_trend(days=30)

            # Plot on chart
            dates = [d['date'] for d in trend]
            counts = [d['total_users'] for d in trend]
        """
        try:
            logger.info(f"Calculating active users trend for last {days} days")

            end_date = timezone.now().date()  # Today: 2026-01-02
            start_date = end_date - timedelta(days=days - 1)  # 7 days ago: 2025-12-27

            logger.info(f"Date range: {start_date} to {end_date}")

            activities = (
                UserActivity.objects.filter(
                    timestamp__date__gte=start_date, timestamp__date__lte=end_date
                )
                .annotate(date=TruncDate("timestamp"))  # contains date part, no time
                .values("date")
                .annotate(
                    # Count distinct registered users
                    registered_users=Count(
                        "user", distinct=True, filter=Q(user__isnull=False)
                    ),
                    # Count distinct anonymous sessions
                    anonymous_users=Count(
                        "session", distinct=True, filter=Q(user__isnull=True)
                    ),
                )
                .order_by("date")
            )

            # Convert queryset to list and add total
            result = []
            for activity in activities:
                total_users = activity["registered_users"]
                if include_anonymous:
                    total_users += activity["anonymous_users"]

                result.append(
                    {
                        "date": activity[
                            "date"
                        ].isoformat(),  # .isoformat() converts datetime.date to string
                        "registered_users": 2,
                        "registered_users": activity["registered_users"],
                        "anonymous_users": (
                            activity["anonymous_users"] if include_anonymous else 0
                        ),
                        "total_users": total_users,
                    }
                )

            # Fill in missing dates with zero counts
            # This ensures the chart has data for every day
            all_dates = [start_date + timedelta(days=x) for x in range(days)]
            # Sets provide O(1) lookup time - checking if a date exists is instant!
            existing_dates = {item["date"] for item in result}

            for date in all_dates:
                date_str = date.isoformat()
                if date_str not in existing_dates:
                    result.append(
                        {
                            "date": date_str,
                            "registered_users": 0,
                            "anonymous_users": 0,
                            "total_users": 0,
                        }
                    )

            # Sort by date
            # Sort each dictionary by its "date" value
            # ISO format dates ("2025-12-27") sort correctly alphabetically!
            result.sort(key=lambda x: x["date"])

            logger.info(f"Active users trend calculated: {len(result)} days of data")

            return result

        except Exception as e:
            logger.error(f"Error calculating active users trend: {str(e)}")
            raise Exception(f"Failed to calculate active users trend: {str(e)}")

    def get_top_performing_content(
        self,
        content_type: Optional[str] = None,
        limit: int = 10,
        metric: str = "views",
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Identify best-performing content across Articles, Jobs, and Events.

        This helps with:
        - Content strategy decisions
        - Featured content selection
        - Editor performance insights
        - SEO prioritization

        Args:
            content_type: "article", "job", "event", or None for all
            limit: Number of items to return (default: 10)
            metric: Sort by "views", "engagement", or "completion"
            date_from: Start date (ISO format)
            date_to: End date (ISO format)

        Returns:
            List of top content items:
            [
                {
                    'content_type': 'article',
                    'content_id': 123,
                    'title': 'Introduction to React Hooks',
                    'views': 15000,
                    'unique_visitors': 12000,
                    'engagement_rate': 8.5,
                    'avg_read_time': 5.2,
                    'completion_rate': 78.5
                },
                ...
            ]

        Example:
            # Get top 10 articles by engagement
            top_articles = analytics_service.get_top_performing_content(
                content_type='article',
                limit=10,
                metric='engagement'
            )

            for article in top_articles:
                print(f"{article['title']}: {article['engagement_rate']}%")
        """
        try:
            logger.info(
                f"Fetching top {limit} {content_type or 'all'} content " f"by {metric}"
            )

            # For articles, we can use ArticleAnalytics which has pre-aggregated data
            if content_type == "article" or content_type is None:
                queryset = ArticleAnalytics.objects.select_related("article")

                if date_from or date_to:
                    if date_from:
                        queryset = queryset.filter(last_updated__gte=date_from)
                    if date_to:
                        queryset = queryset.filter(last_updated__lte=date_to)

                if metric == "views":
                    queryset = queryset.order_by("-total_views")
                elif metric == "engagement":
                    queryset = queryset.order_by("-engagement_rate")
                elif metric == "completion":
                    queryset = queryset.order_by("-completion_rate")
                else:
                    queryset = queryset.order_by("-total_views")

                queryset = queryset[:limit]

                result = []
                for analytics in queryset:
                    result.append(
                        {
                            "content_type": "article",
                            "content_id": analytics.article.id,
                            "title": analytics.article.title,
                            "slug": analytics.article.slug,
                            "views": analytics.total_views,
                            "unique_visitors": analytics.unique_visitors,
                            "engagement_rate": float(analytics.engagement_rate),
                            "avg_read_time": float(analytics.avg_read_time),
                            "completion_rate": float(analytics.completion_rate),
                            "shares": analytics.shares_count,
                            "reactions": analytics.reactions_count,
                            "comments": analytics.comments_count,
                            "saves": analytics.saves_count,
                            "last_updated": analytics.last_updated.isoformat(),
                        }
                    )

                logger.info(f"Found {len(result)} top performing articles")

                return result

            # For other content types (jobs, events), use ContentView
            else:
                queryset = ContentView.objects.filter(content_type=content_type)

                if date_from:
                    queryset = queryset.filter(timestamp__gte=date_from)
                if date_to:
                    queryset = queryset.filter(timestamp__lte=date_to)

                content_stats = (
                    queryset.values("content_type", "content_id")
                    .annotate(
                        total_views=Count("id"),
                        unique_visitors=Count("user", distinct=True),
                        avg_duration=Avg("duration_seconds"),
                    )
                    .order_by("-total_views")[:limit]
                )

                result = []
                for stat in content_stats:
                    result.append(
                        {
                            "content_type": stat["content_type"],
                            "content_id": stat["content_id"],
                            "views": stat["total_views"],
                            "unique_visitors": stat["unique_visitors"],
                            "avg_duration": round(stat["avg_duration"] or 0, 2),
                        }
                    )

                logger.info(f"Found {len(result)} top performing {content_type} items")

                return result

        except Exception as e:
            logger.error(f"Error fetching top performing content: {str(e)}")
            raise Exception(f"Failed to fetch top performing content: {str(e)}")

    def get_dashboard_summary(
        self,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get comprehensive dashboard metrics in a single call.

        This is an optimization method that fetches all key metrics
        at once, reducing the number of API calls needed.

        Args:
            date_from: Start date (ISO format)
            date_to: End date (ISO format)

        Returns:
            Dict with all dashboard metrics:
            {
                'bounce_rate': 45.5,
                'avg_session_duration': 3.2,
                'device_distribution': {...},
                'active_users_trend': [...],
                'top_articles': [...]
            }
        """
        try:
            logger.info("Fetching comprehensive dashboard summary")

            summary = {
                "bounce_rate": self.calculate_bounce_rate(date_from, date_to),
                "avg_session_duration": self.calculate_avg_session_duration(
                    date_from, date_to
                ),
                "device_distribution": self.get_device_distribution(date_from, date_to),
                "active_users_trend": self.get_active_users_trend(days=7),
                "top_articles": self.get_top_performing_content(
                    content_type="article", limit=5, metric="views"
                ),
            }

            logger.info("Dashboard summary fetched successfully")

            return summary

        except Exception as e:
            logger.error(f"Error fetching dashboard summary: {str(e)}")
            raise Exception(f"Failed to fetch dashboard summary: {str(e)}")


analytics_service = AnalyticsService()
