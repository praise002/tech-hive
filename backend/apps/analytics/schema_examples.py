from apps.accounts.schema_examples import UNAUTHORIZED_USER_RESPONSE
from apps.analytics.serializers import DashboardMetricsSerializer, SuccessResponseDataSerializer
from apps.common.errors import ErrorCode
from apps.common.schema_examples import (
    ERR_RESPONSE_STATUS,
    SUCCESS_RESPONSE_STATUS,
    UUID_EXAMPLE,
)
from apps.common.serializers import ErrorDataResponseSerializer, ErrorResponseSerializer
from drf_spectacular.utils import OpenApiExample, OpenApiResponse

# ============================================================================
# EXAMPLE DATA
# ============================================================================

DASHBOARD_METRICS_EXAMPLE = {
    "period": "weekly",
    "date_range": {
        "start": "2025-12-29",
        "end": "2026-01-04",
    },
    "metrics": {
        "time_on_page": {
            "value": 3.5,
            "unit": "minutes",
            "change_percentage": 9.4,
            "trend": "up",
        },
        "bounce_rate": {
            "value": 42,
            "unit": "percentage",
            "change_percentage": 7.6,
            "trend": "down",
        },
        "load_speed": {
            "value": 1.8,
            "unit": "seconds",
            "change_percentage": 14.3,
            "trend": "down",
        },
    },
    "device_types": [
        {"name": "Mobile", "value": 1250, "percentage": 56},
        {"name": "Desktop", "value": 850, "percentage": 38},
        {"name": "Tablet", "value": 150, "percentage": 7},
    ],
    "active_users": [
        {
            "date": "2025-12-29",
            "day": "Mon",
            "registered_users": 89,
            "visitors": 56,
            "total_active_users": 145,
        },
        {
            "date": "2025-12-30",
            "day": "Tue",
            "registered_users": 102,
            "visitors": 65,
            "total_active_users": 167,
        },
        {
            "date": "2025-12-31",
            "day": "Wed",
            "registered_users": 115,
            "visitors": 74,
            "total_active_users": 189,
        },
        {
            "date": "2026-01-01",
            "day": "Thu",
            "registered_users": 128,
            "visitors": 75,
            "total_active_users": 203,
        },
        {
            "date": "2026-01-02",
            "day": "Fri",
            "registered_users": 110,
            "visitors": 68,
            "total_active_users": 178,
        },
        {
            "date": "2026-01-03",
            "day": "Sat",
            "registered_users": 95,
            "visitors": 61,
            "total_active_users": 156,
        },
        {
            "date": "2026-01-04",
            "day": "Sun",
            "registered_users": 88,
            "visitors": 54,
            "total_active_users": 142,
        },
    ],
    "top_performing_posts": [
        {
            "category": "Articles",
            "views": 1250,
            "shares": 45,
            "title": "Django REST Framework Complete Guide",
            "id": "550e8400-e29b-41d4-a716-446655440001",
        },
        {
            "category": "Jobs",
            "views": 850,
            "shares": 30,
            "title": "Senior Django Developer at TechCorp",
            "id": "550e8400-e29b-41d4-a716-446655440002",
        },
        {
            "category": "Events",
            "views": 650,
            "shares": 35,
            "title": "Tech Conference 2026",
            "id": "550e8400-e29b-41d4-a716-446655440003",
        },
    ],
    "cached": False,
}


DASHBOARD_METRICS_CACHED_EXAMPLE = {
    **DASHBOARD_METRICS_EXAMPLE,
    "cached": True,
}

DASHBOARD_METRICS_MONTHLY_EXAMPLE = {
    "period": "monthly",
    "date_range": {
        "start": "2025-12-05",
        "end": "2026-01-04",
    },
    "metrics": {
        "time_on_page": {
            "value": 4.2,
            "unit": "minutes",
            "change_percentage": 10.5,
            "trend": "up",
        },
        "bounce_rate": {
            "value": 39,
            "unit": "percentage",
            "change_percentage": 8.6,
            "trend": "down",
        },
        "load_speed": {
            "value": 1.6,
            "unit": "seconds",
            "change_percentage": 15.8,
            "trend": "down",
        },
    },
    "device_types": [
        {"name": "Mobile", "value": 5200, "percentage": 58},
        {"name": "Desktop", "value": 3100, "percentage": 35},
        {"name": "Tablet", "value": 615, "percentage": 7},
    ],
    "active_users": [
        {
            "date": "2025-12-05",
            "day": "Thu",
            "registered_users": 280,
            "visitors": 140,
            "total_active_users": 420,
        },
        {
            "date": "2025-12-06",
            "day": "Fri",
            "registered_users": 295,
            "visitors": 150,
            "total_active_users": 445,
        },
        {
            "date": "2025-12-07",
            "day": "Sat",
            "registered_users": 310,
            "visitors": 160,
            "total_active_users": 470,
        },
        {
            "date": "2025-12-08",
            "day": "Sun",
            "registered_users": 290,
            "visitors": 145,
            "total_active_users": 435,
        },
        {
            "date": "2025-12-09",
            "day": "Mon",
            "registered_users": 320,
            "visitors": 170,
            "total_active_users": 490,
        },
        {
            "date": "2025-12-10",
            "day": "Tue",
            "registered_users": 335,
            "visitors": 180,
            "total_active_users": 515,
        },
        # ... showing 6 days for brevity, would have 30 total
        {
            "date": "2026-01-04",
            "day": "Sun",
            "registered_users": 350,
            "visitors": 180,
            "total_active_users": 530,
        },
    ],
    "top_performing_posts": [
        {
            "category": "Articles",
            "views": 5400,
            "shares": 185,
            "title": "Django REST Framework Complete Guide",
            "id": "550e8400-e29b-41d4-a716-446655440001",
        },
        {
            "category": "Jobs",
            "views": 3600,
            "shares": 120,
            "title": "Senior Django Developer at TechCorp",
            "id": "550e8400-e29b-41d4-a716-446655440002",
        },
        {
            "category": "Events",
            "views": 2800,
            "shares": 150,
            "title": "Tech Conference 2026",
            "id": "550e8400-e29b-41d4-a716-446655440003",
        },
    ],
    "cached": False,
}


TRACK_ACTIVITY_REQUEST_EXAMPLE = {
    "event_type": "page_view",
    "session_id": "session-abc-123-def-456",
    "page_url": "https://techhive.com/articles/django-tips/",
    "referrer": "https://google.com/search?q=django+tips",
    "device_type": "Mobile",
    "browser": "Chrome",
    "browser_version": "120.0.6099",
    "os": "Android",
    "os_version": "14",
    "screen_resolution": "1080x2400",
    "duration_seconds": 180,
    "load_time_ms": 1250,
    "metadata": {
        "content_type": "article",
        "content_id": "550e8400-e29b-41d4-a716-446655440000",
    },
}

TRACK_ACTIVITY_SUCCESS_EXAMPLE = {
    "activity_id": UUID_EXAMPLE,
}

ARTICLE_ANALYTICS_EXAMPLE = {
    "article_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Django REST Framework Complete Guide",
    "total_views": 1250,
    "unique_visitors": 890,
    "total_shares": 45,
    "avg_time_on_page": 3.5,
    "bounce_rate": 42.3,
    "period": "weekly",
    "date_range": {
        "start": "2025-12-29T00:00:00Z",
        "end": "2026-01-04T23:59:59Z",
    },
    "cached": False,
}

ARTICLE_ANALYTICS_MONTHLY_EXAMPLE = {
    "article_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Django REST Framework Complete Guide",
    "total_views": 5400,
    "unique_visitors": 3850,
    "total_shares": 185,
    "avg_time_on_page": 4.2,
    "bounce_rate": 38.5,
    "period": "monthly",
    "date_range": {
        "start": "2025-12-05T00:00:00Z",
        "end": "2026-01-04T23:59:59Z",
    },
    "cached": False,
}

# ============================================================================
# RESPONSE EXAMPLES
# ============================================================================

DASHBOARD_METRICS_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=DashboardMetricsSerializer,
        description="Dashboard metrics retrieved successfully",
        examples=[
            OpenApiExample(
                name="Weekly Metrics (Fresh)",
                summary="Freshly calculated weekly metrics",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Dashboard metrics calculated successfully",
                    "data": DASHBOARD_METRICS_EXAMPLE,
                },
            ),
            OpenApiExample(
                name="Weekly Metrics (Cached)",
                summary="Cached weekly metrics",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Dashboard metrics calculated successfully",
                    "data": DASHBOARD_METRICS_CACHED_EXAMPLE,
                },
            ),
            OpenApiExample(
                name="Monthly Metrics",
                summary="Monthly analytics with 30 days of data",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Dashboard metrics calculated successfully",
                    "data": DASHBOARD_METRICS_MONTHLY_EXAMPLE,
                },
            ),
        ],
    ),
    400: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Invalid period parameter",
        examples=[
            OpenApiExample(
                name="Invalid Period",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": 'Invalid period "daily". Must be "weekly" or "monthly"',
                    "code": ErrorCode.BAD_REQUEST,
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    403: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Permission denied - Admin only",
        examples=[
            OpenApiExample(
                name="Not Admin",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "You do not have permission to perform this action.",
                    "code": ErrorCode.FORBIDDEN,
                },
            ),
        ],
    ),
}

TRACK_ACTIVITY_RESPONSE_EXAMPLE = {
    201: OpenApiResponse(
        response=SuccessResponseDataSerializer,
        description="Activity tracked successfully",
        examples=[
            OpenApiExample(
                name="Page View Tracked",
                summary="Successfully tracked a page view event",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Activity tracked successfully",
                    "data": TRACK_ACTIVITY_SUCCESS_EXAMPLE,
                },
            ),
        ],
    ),
    422: ErrorDataResponseSerializer,
}

ARTICLE_ANALYTICS_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=SuccessResponseDataSerializer,
        description="Article analytics retrieved successfully",
        examples=[
            OpenApiExample(
                name="Weekly Analytics",
                summary="Weekly analytics for a specific article",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Article analytics retrieved successfully",
                    "data": ARTICLE_ANALYTICS_EXAMPLE,
                },
            ),
            OpenApiExample(
                name="Monthly Analytics",
                summary="Monthly analytics with more data points",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Article analytics retrieved successfully",
                    "data": ARTICLE_ANALYTICS_MONTHLY_EXAMPLE,
                },
            ),
        ],
    ),
    400: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Invalid period parameter",
        examples=[
            OpenApiExample(
                name="Invalid Period",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": 'Invalid period "yearly". Must be "weekly" or "monthly"',
                    "code": ErrorCode.BAD_REQUEST,
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    403: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Permission denied - Not author or admin",
        examples=[
            OpenApiExample(
                name="Not Author or Admin",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "You do not have permission to view this article's analytics.",
                    "code": ErrorCode.FORBIDDEN,
                },
            ),
        ],
    ),
    404: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Article not found",
        examples=[
            OpenApiExample(
                name="Article Not Found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Article not found",
                    "code": ErrorCode.NON_EXISTENT,
                },
            ),
        ],
    ),
}
