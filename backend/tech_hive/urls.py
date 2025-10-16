from apps.common.responses import CustomResponse
from apps.common.serializers import SuccessResponseSerializer
from apps.content.sitemaps import ArticleSitemap
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import JsonResponse
from django.urls import include, path
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import status
from rest_framework.views import APIView


class HealthCheckView(APIView):
    """
    API Health Check
    This endpoint checks the health of the API
    """

    serializer_class = None

    @extend_schema(
        "/",
        summary="API Health Check",
        description="This endpoint checks the health of the API",
        responses=SuccessResponseSerializer,
        tags=["HealthCheck"],
        auth=[],
    )
    def get(self, request):

        return CustomResponse.success(message="pong", status_code=status.HTTP_200_OK)


def handler404(request, exception=None):
    """
    Custom 404 handler
    """
    response = JsonResponse({"status": "failure", "message": "Not Found"})
    response.status_code = 404
    return response


def handler500(request, exception=None):
    """
    Custom 500 handler
    """
    response = JsonResponse({"status": "failure", "message": "Server Error"})
    response.status_code = 500
    return response


handler404 = handler404
handler500 = handler500

sitemaps = {
    "articles": ArticleSitemap,
}

from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.general.urls")),
    path("api/v1/", include("apps.content.urls")),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/profiles/", include("apps.profiles.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/v1/healthcheck/", HealthCheckView.as_view()),
]

urlpatterns += [
    path("ckeditor5/", include("django_ckeditor_5.urls")),
]

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
    urlpatterns += [path("prometheus/", include("django_prometheus.urls"))]
