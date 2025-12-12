from django.urls import path

from . import views

urlpatterns = [
    path(
        "plans/",
        views.SubscriptionPlanListView.as_view(),
    ),
    path(
        "me/",
        views.SubscriptionDetailView.as_view(),
    ),
    path(
        "payment-history/",
        views.PaymentHistoryListView.as_view(),
    ),
    path(
        "premium/",
        views.SubscribeToPremiumView.as_view(),
    ),
    path(
        "premium/",
        views.SubscriptionCancelAPIView.as_view(),
    ),
]
