from django.urls import path

from .views import ArticlePerformanceView, DashboardMetricsView, TrackActivityView

app_name = "analytics"

urlpatterns = [
    path("dashboard/", DashboardMetricsView.as_view()),
    path("track/", TrackActivityView.as_view()),
    path("articles/<uuid:article_id>/", ArticlePerformanceView.as_view()),
]
