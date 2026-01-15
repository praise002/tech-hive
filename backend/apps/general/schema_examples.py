from apps.common.errors import ErrorCode
from apps.common.schema_examples import (
    AVATAR_URL,
    ERR_RESPONSE_STATUS,
    SUCCESS_RESPONSE_STATUS,
)
from apps.common.serializers import ErrorDataResponseSerializer, ErrorResponseSerializer
from apps.general.serializer import (
    ContactSerializer,
    NewsletterSerializer,
    SiteDetailSerializer,
)
from drf_spectacular.utils import OpenApiExample, OpenApiResponse

SITE_DETAIL_EXAMPLE = {
    "image_url": AVATAR_URL,
    "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    "fb": "https://facebook.com",
    "ln": "https://linkedin.com",
    "x": "https://x.com",
    "ig": "https://instagram.com",
}

SUBSCRIBE_RESPONSE_EXAMPLE = {
    201: OpenApiResponse(
        response=NewsletterSerializer,
        description="Subscription Successful",
        examples=[
            OpenApiExample(
                name="Subscription Successful",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Subscribed to newsletter successfully.",
                },
            ),
        ],
    ),
    422: OpenApiResponse(
        response=ErrorDataResponseSerializer,
        description="Validation Error",
    ),
}

UNSUBSCRIBE_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=NewsletterSerializer,
        description="Unsubscription Successful",
        examples=[
            OpenApiExample(
                name="Unsubscription Successful",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "You have been unsubscribed from our newsletter.",
                },
            ),
        ],
    ),
    404: OpenApiResponse(
        description="Subscription not found",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Subscription Not Found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Invalid unsubscribe link or already unsubscribed.",
                    "code": ErrorCode.NON_EXISTENT,
                },
            ),
        ],
    ),
}

SITE_DETAIL_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=SiteDetailSerializer,
        description="Site Detail Retrieval Successful",
        examples=[
            OpenApiExample(
                name="Site Detail Retrieval Successful",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Site detail retrieved successfully.",
                    "data": SITE_DETAIL_EXAMPLE,
                },
            ),
        ],
    ),
}

CONTACT_RESPONSE_EXAMPLE = {
    201: OpenApiResponse(
        response=ContactSerializer,
        description="Message Sent Successful",
        examples=[
            OpenApiExample(
                name="Message Sent Successful",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Message sent successfully.",
                },
            ),
        ],
    ),
    422: OpenApiResponse(
        response=ErrorDataResponseSerializer,
        description="Validation Error",
    ),
}
