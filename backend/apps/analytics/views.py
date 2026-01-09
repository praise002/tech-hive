from datetime import datetime, time, timedelta

from apps.analytics.analytics_service import AnalyticsService
from apps.analytics.choices import EventTypeChoices
from apps.analytics.permissions import IsAuthorOrAdmin
from apps.analytics.schema_examples import (
    ARICLE_ANALYTICS_EXPORT_RESPONSE,
    ARTICLE_ANALYTICS_RESPONSE_EXAMPLE,
    DASHBOARD_EXPORT_RESPONSE,
    DASHBOARD_METRICS_RESPONSE_EXAMPLE,
    TRACK_ACTIVITY_REQUEST_EXAMPLE,
    TRACK_ACTIVITY_RESPONSE_EXAMPLE,
)
from apps.analytics.utils import analytics_exporter
from apps.common.errors import ErrorCode
from apps.common.exceptions import NotFoundError
from apps.common.responses import CustomResponse
from apps.content.models import Article
from django.core.cache import cache
from django.db.models import Avg
from django.http import HttpResponse
from django.utils import timezone
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from .models import SessionMetrics, UserActivity
from .serializers import (
    DashboardMetricsSerializer,
    SuccessResponseDataSerializer,
    TrackActivityRequestSerializer,
)

tags = ["Analytics"]


class DashboardMetricsView(APIView):
    """
    GET /api/analytics/dashboard/?period=weekly

    Returns complete dashboard metrics:
    - Time on page, bounce rate, load speed (with trends)
    - Device distribution
    - Active users timeline
    - Top performing posts
    """

    permission_classes = (IsAdminUser,)
    serializer_class = DashboardMetricsSerializer

    @extend_schema(
        summary="Retrieve dashboard analytics metrics",
        description=(
            "This endpoint provides comprehensive analytics metrics for the entire platform. "
            "It includes key performance indicators (KPIs) such as average time on page, bounce rate, "
            "and page load speed, with trend comparisons to the previous period. "
            "Also includes device distribution, daily active user timeline, and top-performing content "
            "across different categories (tutorials, news, events). "
            "\n\n**Available Periods:**\n"
            "- `weekly`: Last 7 days compared to previous 7 days\n"
            "- `monthly`: Last 30 days compared to previous 30 days\n"
            "\n**Caching:** Results are cached and invalidated at midnight per period to improve performance."
        ),
        parameters=[
            OpenApiParameter(
                name="period",
                description="Time period for analytics calculation",
                enum=["weekly", "monthly"],
                default="weekly",
                required=False,
            ),
        ],
        tags=tags,
        responses=DASHBOARD_METRICS_RESPONSE_EXAMPLE,
    )
    def get(self, request):
        period = request.query_params.get("period", "weekly").lower()

        if period not in ["weekly", "monthly"]:
            return CustomResponse.error(
                message='Invalid period. Must be "weekly" or "monthly"',
                err_code=ErrorCode.BAD_REQUEST,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        cache_key = f"dashboard_metrics:{period}:{timezone.now().date()}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return CustomResponse.success(
                message="Dashboard metrics calculated successfully",
                data={
                    **cached_data,
                    "cached": True,
                },
            )

        data = AnalyticsService.get_dashboard_metrics(period)

        now = timezone.now()
        midnight = datetime.combine(
            now.date() + timedelta(days=1), time.min, tzinfo=now.tzinfo
        )
        seconds_until_midnight = int((midnight - now).total_seconds())

        # Cache until midnight (then auto-expires)
        cache.set(cache_key, data, seconds_until_midnight)

        return CustomResponse.success(
            message="Dashboard metrics calculated successfully",
            data={
                **data,
                "cached": False,
            },
        )


class TrackActivityView(APIView):
    """
    POST /api/analytics/track/

    Accepts analytics events from frontend.
    Creates UserActivity records.

    Payload example:
    {
        "event_type": "page_view",
        "session_id": "session-uuid",
        "page_url": "/articles/django-tips/",
        "device_type": "Mobile",
        "duration_seconds": 120,
        "metadata": {
            "content_type": "article",
            "content_id": "article-uuid"
        }
    }
    """

    serializer_class = SuccessResponseDataSerializer

    @extend_schema(
        summary="Track user activity event",
        description=(
            "This endpoint accepts analytics events from the frontend to track user interactions. "
            "It creates activity records linked to sessions and handles various event types including "
            "page views, page loads, and social shares. "
            "\n\n**Event Types:**\n"
            "- `page_view`: User viewed a page\n"
            "- `page_load`: Page finished loading (includes load time)\n"
            "- `share`: User shared content\n"
            "\n**Note:** This endpoint is publicly accessible to allow tracking for anonymous users."
        ),
        request=TrackActivityRequestSerializer,
        examples=[
            OpenApiExample(
                name="Page View with Metadata",
                summary="Track article page view",
                description="Example of tracking a page view with content metadata",
                value=TRACK_ACTIVITY_REQUEST_EXAMPLE,
                request_only=True,
            ),
            OpenApiExample(
                name="Share Event",
                summary="Track content share",
                value={
                    "event_type": "share",
                    "session_id": "session-abc-123",
                    "page_url": "https://techhive.com/articles/django-tips/",
                    "device_type": "Desktop",
                    "metadata": {
                        "content_type": "article",
                        "content_id": "550e8400-e29b-41d4-a716-446655440000",
                        "share_platform": "twitter",
                    },
                },
                request_only=True,
            ),
        ],
        tags=tags,
        auth=[],
        responses=TRACK_ACTIVITY_RESPONSE_EXAMPLE,
    )
    def post(self, request):
        serializer = TrackActivityRequestSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        session_id = validated_data["session_id"]
        session, created = SessionMetrics.objects.get_or_create(
            session_id=session_id,
            defaults={  # ← Used ONLY if creating new record
                "user": request.user if request.user.is_authenticated else None,
                "device_type": validated_data.get("device_type", None),
            },
        )

        # Handle anonymous → authenticated transition
        # This helps preserve one SessionMetrics while userLogin will show the pre-login stages
        if not created and request.user.is_authenticated and not session.user:
            session.user = request.user
            session.save(update_fields=["user"])

        activity = UserActivity.objects.create(
            session=session,
            user=request.user if request.user.is_authenticated else None,
            event_type=validated_data["event_type"],
            page_url=validated_data["page_url"],
            referrer=validated_data.get("referrer", None),
            device_type=validated_data.get("device_type"),
            browser=validated_data.get("browser"),
            browser_version=validated_data.get("browser_version"),
            os=validated_data.get("os"),
            os_version=validated_data.get("os_version"),
            screen_resolution=validated_data.get("screen_resolution"),
            duration_seconds=validated_data.get("duration_seconds", 0),
            load_time_ms=validated_data.get("load_time_ms"),
            metadata=validated_data.get("metadata", {}),
        )

        session.page_count += 1
        session.is_bounce = session.page_count == 1
        session.save(update_fields=["page_count", "is_bounce"])

        return CustomResponse.success(
            message="Activity tracked successfully",
            data={"activity_id": str(activity.id)},
            status_code=status.HTTP_201_CREATED,
        )


class ArticlePerformanceView(APIView):
    """
    GET /api/analytics/articles/{article_id}/?period=weekly

    Returns detailed analytics for a specific article:
    - Total views
    - Unique visitors
    - Shares
    - Average time on page
    - Bounce rate
    """

    permission_classes = (IsAuthorOrAdmin,)
    serializer_class = SuccessResponseDataSerializer

    @extend_schema(
        summary="Retrieve analytics for a specific article",
        description=(
            "This endpoint provides detailed performance analytics for a specific article. "
            "It includes metrics such as total views, unique visitors, shares, average time on page, "
            "and bounce rate. "
            "\n\n**Access Control:**\n"
            "- Article authors can view their own article analytics\n"
            "- Site administrators can view analytics for any article\n"
            "\n**Available Periods:**\n"
            "- `weekly`: Last 7 days of analytics data\n"
            "- `monthly`: Last 30 days of analytics data\n"
            "\n**Bounce Rate Calculation:**\n"
            "Percentage of sessions that viewed only this article and then left the site without "
            "viewing any other pages.\n"
            "\n**Caching:** Results are cached for and invalidated at midnight per article and period."
        ),
        parameters=[
            OpenApiParameter(
                name="period",
                description="Time period for analytics calculation",
                enum=["weekly", "monthly"],
                default="weekly",
                required=False,
            ),
        ],
        tags=tags,
        responses=ARTICLE_ANALYTICS_RESPONSE_EXAMPLE,
    )
    def get(self, request, article_id):
        period = request.query_params.get("period", "weekly").lower()

        if period not in ["weekly", "monthly"]:
            return CustomResponse.error(
                message='Invalid period. Must be "weekly" or "monthly"',
                err_code=ErrorCode.BAD_REQUEST,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            raise NotFoundError("Article not found")

        self.check_object_permissions(request, article)

        date_range = AnalyticsService.get_date_range(period)
        start_date = date_range["current_start"]
        end_date = date_range["current_end"]

        views_data = UserActivity.objects.filter(
            event_type=EventTypeChoices.PAGE_VIEW,
            timestamp__date__gte=start_date,
            timestamp__date__lte=end_date,
            metadata__content_type="article",
            metadata__content_id=str(article_id),
        )
        total_views = views_data.count()
        unique_visitors = views_data.values("session").distinct().count()
        avg_time = views_data.aggregate(avg=Avg("duration_seconds"))["avg"] or 0

        total_shares = UserActivity.objects.filter(
            event_type=EventTypeChoices.SHARE,
            timestamp__date__gte=start_date,
            timestamp__date__lte=end_date,
            metadata__content_type="article",
            metadata__content_id=str(article_id),
        ).count()

        sessions_with_views = views_data.values_list("session_id", flat=True).distinct()
        bounced_sessions = SessionMetrics.objects.filter(
            id__in=sessions_with_views, is_bounce=True
        ).count()

        bounce_rate = (
            (bounced_sessions / len(sessions_with_views) * 100)
            if sessions_with_views
            else 0
        )

        cache_key = f"article:{period}:{article_id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return CustomResponse.success(
                message="Article analytics retrieved successfully",
                data={
                    **cached_data,
                    "cached": True,
                },
            )

        data = {
            "article_id": str(article_id),
            "title": article.title,
            "total_views": total_views,
            "unique_visitors": unique_visitors,
            "total_shares": total_shares,
            "avg_time_on_page": round(avg_time / 60, 1),  # Convert to minutes
            "bounce_rate": round(bounce_rate, 0),
            "period": period,
            "date_range": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
            },
        }

        now = timezone.now()
        midnight = datetime.combine(
            now.date() + timedelta(days=1), time.min, tzinfo=now.tzinfo
        )
        seconds_until_midnight = int((midnight - now).total_seconds())

        # Cache until midnight (then auto-expires)
        cache.set(cache_key, data, seconds_until_midnight)

        return CustomResponse.success(
            message="Article analytics retrieved successfully",
            data={
                **data,
                "cached": False,
            },
        )


class DashboardExportView(APIView):
    """
    GET /api/analytics/dashboard/export/?period=weekly&format=csv

    Export dashboard metrics to CSV or Excel
    """
    # from rest_framework.renderers import JSONRenderer

    permission_classes = (IsAdminUser,)
    serializer_class = None
    # renderer_classes = [JSONRenderer]
    
    
    
    # def finalize_response(self, request, response, *args, **kwargs):
    #     # For file downloads (HttpResponse), return as-is
    #     if isinstance(response, HttpResponse):
    #         return response
    #     # For DRF Response objects (errors), process normally
    #     return super().finalize_response(request, response, *args, **kwargs)

    @extend_schema(
        summary="Export dashboard metrics",
        description=(
            "Export comprehensive dashboard analytics to CSV or Excel format. "
            "Includes all metrics, device distribution, active users timeline, and top posts."
        ),
        parameters=[
            OpenApiParameter(
                name="period",
                description="Time period for analytics",
                enum=["weekly", "monthly"],
                default="weekly",
                required=False,
            ),
            OpenApiParameter(
                name="format",
                description="Export file format",
                enum=["csv", "excel"],
                default="csv",
                required=False,
            ),
        ],
        tags=tags,
        responses=DASHBOARD_EXPORT_RESPONSE,
    )
    def get(self, request):
        period = request.query_params.get("period", "weekly").lower()
        export_format = request.query_params.get("format", "csv").lower()

        if period not in ["weekly", "monthly"]:
            # return CustomResponse.error(
            #     message='Invalid period. Must be "weekly" or "monthly"',
            #     err_code=ErrorCode.BAD_REQUEST,
            #     status_code=status.HTTP_400_BAD_REQUEST,
            # )
            pass

        if export_format not in ["csv", "excel"]:
            # return CustomResponse.error(
            #     message='Invalid format. Must be "csv" or "excel"',
            #     err_code=ErrorCode.BAD_REQUEST,
            #     status_code=status.HTTP_400_BAD_REQUEST,
            # )
            pass

        data = AnalyticsService.get_dashboard_metrics(period)

        if export_format == "csv":
            return analytics_exporter.export_dashboard_to_csv(data)
        else:
            return analytics_exporter.export_dashboard_to_excel(data)


class ArticleAnalyticsExportView(APIView):
    """
    GET /api/analytics/articles/{article_id}/export/?period=weekly&format=csv

    Export article analytics to CSV
    """

    permission_classes = (IsAuthorOrAdmin,)
    serializer_class = None

    @extend_schema(
        summary="Export article analytics",
        description=(
            "Export detailed analytics for a specific article to CSV format. "
            "Includes views, visitors, shares, time on page, and bounce rate."
        ),
        parameters=[
            OpenApiParameter(
                name="period",
                description="Time period for analytics",
                enum=["weekly", "monthly"],
                default="weekly",
                required=False,
            ),
            OpenApiParameter(
                name="format",
                description="Export file format",
                enum=["csv"],
                default="csv",
                required=False,
            ),
        ],
        tags=tags,
        responses=ARICLE_ANALYTICS_EXPORT_RESPONSE,
    )
    def get(self, request, article_id):
        period = request.query_params.get("period", "weekly").lower()
        export_format = request.query_params.get("format", "csv").lower()

        if period not in ["weekly", "monthly"]:
            return CustomResponse.error(
                message='Invalid period. Must be "weekly" or "monthly"',
                err_code=ErrorCode.BAD_REQUEST,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        if export_format != "csv":
            return CustomResponse.error(
                message='Invalid format. Must be "csv"',
                err_code=ErrorCode.BAD_REQUEST,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            raise NotFoundError("Article not found")

        self.check_object_permissions(request, article)

        date_range = AnalyticsService.get_date_range(period)
        start_date = date_range["current_start"]
        end_date = date_range["current_end"]

        views_data = UserActivity.objects.filter(
            event_type=EventTypeChoices.PAGE_VIEW,
            timestamp__gte=start_date,
            timestamp__lte=end_date,
            metadata__content_type="article",
            metadata__content_id=str(article_id),
        )

        total_views = views_data.count()
        unique_visitors = views_data.values("session").distinct().count()
        avg_time = views_data.aggregate(avg=Avg("duration_seconds"))["avg"] or 0

        total_shares = UserActivity.objects.filter(
            event_type=EventTypeChoices.SHARE,
            timestamp__gte=start_date,
            timestamp__lte=end_date,
            metadata__content_type="article",
            metadata__content_id=str(article_id),
        ).count()

        sessions_with_views = views_data.values_list("session_id", flat=True).distinct()
        bounced_sessions = SessionMetrics.objects.filter(
            id__in=sessions_with_views, is_bounce=True
        ).count()

        bounce_rate = (
            (bounced_sessions / len(sessions_with_views) * 100)
            if sessions_with_views
            else 0
        )

        data = {
            "article_id": str(article_id),
            "title": article.title,
            "total_views": total_views,
            "unique_visitors": unique_visitors,
            "total_shares": total_shares,
            "avg_time_on_page": round(avg_time / 60, 1),
            "bounce_rate": round(bounce_rate, 0),
            "period": period,
            "date_range": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
            },
        }

        return analytics_exporter.export_article_analytics_to_csv(data)
