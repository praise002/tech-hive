from apps.common.schema_examples import AVATAR_URL, SUCCESS_RESPONSE_STATUS
from apps.common.serializers import ErrorDataResponseSerializer
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
    204: OpenApiResponse(
        response=None,
        description="Unsubscription Successful",
    ),
    422: OpenApiResponse(
        response=ErrorDataResponseSerializer,
        description="Validation Error",
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
