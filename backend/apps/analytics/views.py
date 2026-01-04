from apps.content.models import Article
from django.core.cache import cache
from django.db.models import Avg, Count
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.apps.analytics import analytics_service
from backend.apps.analytics.choices import EventTypeChoices
from backend.apps.analytics.permissions import IsAuthorOrAdmin
from backend.apps.common.errors import ErrorCode
from backend.apps.common.exceptions import NotFoundError
from backend.apps.common.responses import CustomResponse

from .models import SessionMetrics, UserActivity
from .serializers import DashboardMetricsSerializer, TrackActivitySerializer


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

    def get(self, request):
        period = request.query_params.get("period", "weekly")

        if period not in ["weekly", "monthly"]:
            return CustomResponse.error(
                message='Invalid period. Must be "weekly" or "monthly"',
                err_code=ErrorCode.BAD_REQUEST,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # TODO:
        # Check cache first (cache for 5 minutes)
        # cache_key = f"dashboard_metrics:{period}"
        # cached_data = cache.get(cache_key)

        # if cached_data:
        #     return Response({"status": "success", "data": cached_data, "cached": True})

        # Calculate metrics

        data = analytics_service.get_dashboard_metrics(period)

        # Cache the result
        # cache.set(cache_key, data, 300)  # 5 minutes

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

    serializer_class = None

    def post(self, request):
        serializer = TrackActivitySerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        session_id = validated_data["session_id"]
        session, _ = SessionMetrics.objects.get_or_create(
            session_id=session_id,
            defaults={  # ← Used ONLY if creating new record
                "user": request.user if request.user.is_authenticated else None,
                "device_type": validated_data.get("device_type", None),
            },
        )
        
        # Handle anonymous → authenticated transition
        # if not created and request.user.is_authenticated and not session.user:
        #     session.user = request.user
        #     session.save(update_fields=["user"])

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

        def get(self, request, article_id):
            period = request.query_params.get("period", "weekly")

            try:
                article = Article.objects.get(id=article_id)
            except Article.DoesNotExist:
                return NotFoundError("Article not found")

            date_range = analytics_service.get_date_range(period)
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

            sessions_with_views = views_data.values_list(
                "session_id", flat=True
            ).distinct()
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
                "avg_time_on_page": round(avg_time / 60, 1),  # Convert to minutes
                "bounce_rate": round(bounce_rate, 1),
                "period": period,
                "date_range": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat(),
                },
            }

            return CustomResponse.success(
                message="",
                **data,
            )
