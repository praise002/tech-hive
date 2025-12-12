from apps.accounts.schema_examples import UNAUTHORIZED_USER_RESPONSE
from apps.common.errors import ErrorCode
from apps.common.schema_examples import ERR_RESPONSE_STATUS, SUCCESS_RESPONSE_STATUS
from apps.common.serializers import ErrorDataResponseSerializer, ErrorResponseSerializer, SuccessDataResponseSerializer
from apps.subscriptions.serializers import (
    SubscriptionDetailSerializer,
    SubscriptionPlanSerializer,
)
from drf_spectacular.utils import OpenApiExample, OpenApiResponse

SUBSCRIPTION_DETAIL_EXAMPLE = {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "status": "TRIALING",
    "plan": {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "Premium Monthly",
        "description": "Full access to premium features",
        "price": "4991.40",
        "billing_cycle": "MONTHLY",
        "features": "access,priority-support",
    },
    "is_premium": True,
    "is_trial": True,
    "trial_start": "2025-12-12T08:25:26.823Z",
    "trial_end": "2025-12-19T08:25:26.823Z",
    "current_period_start": "2025-12-12T08:25:26.823Z",
    "current_period_end": "2026-01-12T08:25:26.823Z",
    "next_billing_date": "2026-01-12T08:25:26.823Z",
    "days_remaining": 30,
    "cancelled_at": None,
    "cancel_at_period_end": False,
    "is_in_grace_period": False,
    "grace_period_ends_at": None,
    "card_details": {"last4": "4081", "type": "visa", "bank": "GTBank"},
}

SUBSCRIPTION_PLAN_EXAMPLE = [
    {
        "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "name": "Premium Monthly",
        "description": "Get full access to all our premium features, billed monthly.",
        "price": "5000.00",
        "billing_cycle": "MONTHLY",
        "features": {
            "article_limit": "unlimited",
            "support_level": "priority",
            "early_access": True,
        },
    },
    {
        "id": "f1e2d3c4-b5a6-7890-1234-567890fedcba",
        "name": "Premium Yearly",
        "description": "Save 20% with our annual plan and get full access to all premium features.",
        "price": "50000.00",
        "billing_cycle": "YEARLY",
        "features": {
            "article_limit": "unlimited",
            "support_level": "priority",
            "early_access": True,
        },
    },
]

SUBSCRIPTION_DETAIL_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Subscription Retrieve Successful",
        response=SubscriptionDetailSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Subscription retrieved successfully",
                    "data": SUBSCRIPTION_DETAIL_EXAMPLE,
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    404: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Subscription not found",
        examples=[
            OpenApiExample(
                name="Subscription not found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Subscription not found",
                    "code": ErrorCode.NON_EXISTENT,
                },
            ),
        ],
    ),
}

PAYMENT_HISTORY_RESPONSE_EXAMPLE = {
    401: UNAUTHORIZED_USER_RESPONSE,
}

SUBSCRIPTION_PLAN_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Subscription Plans Retrieve Successful",
        response=SubscriptionPlanSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Subscription plans retrieved successfully",
                    "data": SUBSCRIPTION_PLAN_EXAMPLE,
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
}


SUBSCRIBE_TO_PREMIUM_RESPONSE_EXAMPLE = {
    201: OpenApiResponse(
        description="Subscription Created/Initialized Successfully. The response body will vary depending on whether a trial was started or a paid subscription was initialized.",
        response=SuccessDataResponseSerializer,
        examples=[
            OpenApiExample(
                name="Trial Started Successfully",
                summary="Response when a trial is started.",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "7-day trial started successfully.",
                    "data": {
                        "status": "TRIALING",
                        "trial_end": "2025-12-19T10:30:00Z",
                    },
                },
            ),
            OpenApiExample(
                name="Paid Subscription Initialized",
                summary="Response when a paid subscription is created, providing a payment link.",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Subscription initialized. Please proceed to payment.",
                    "data": {
                        "authorization_url": "https://checkout.paystack.com/b3i6x28wstbt5na"
                    },
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    422: ErrorDataResponseSerializer,
}
