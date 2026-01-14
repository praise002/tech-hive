from django.urls import path

from . import views

urlpatterns = [
    path("notifications/", views.NotificationListView.as_view()),
    path(
        "notifications/<uuid:pk>/",
        views.NotificationDetailView.as_view(),
    ),
    path(
        "notifications/<uuid:pk>/restore/",
        views.NotificationRestoreView.as_view(),
    ),
]
