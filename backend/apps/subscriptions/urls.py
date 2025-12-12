from django.urls import path

from . import views
from .webhooks import webhook as wh

urlpatterns = [
    # Subscription Plans
    path(
        "plans/",
        views.SubscriptionPlanListView.as_view(),
    ),
    # Subscription Management
    path(
        "me/",
        views.SubscriptionDetailView.as_view(),
    ),
    path(
        "premium/",
        views.SubscribeToPremiumView.as_view(),
    ),
    path(
        "premium/",
        views.SubscriptionCancelAPIView.as_view(),
    ),
    path(
        "reactivate/",
        views.ReactivateSubscriptionView.as_view(),
    ),
    # Payment
    path(
        "payment/callback/",
        views.PaymentCallbackView.as_view(),
    ),
    path("payment-retry/", views.RetryPaymentView.as_view()),
    path("card-update/", views.UpdatePaymentMethodView.as_view()),
    path(
        "payment-history/",
    views.PaymentHistoryListView.as_view(),
    ),
    # Webhook
    path("webhook/", wh),
]
