from apps.accounts.schema_examples import UNAUTHORIZED_USER_RESPONSE
from apps.common.schema_examples import SUCCESS_RESPONSE_STATUS, UUID_EXAMPLE
from apps.content.serializers import (
    CategorySerializer,
    ContributorOnboardingSerializer,
    TagSerializer,
)
from drf_spectacular.utils import OpenApiExample, OpenApiResponse

from apps.common.serializers import ErrorDataResponseSerializer

CATEGORY_LIST_EXAMPLE = {
    "id": UUID_EXAMPLE,
    "name": "Technology",
    "slug": "technology",
    "desc": "All articles and tutorials related to technology and innovation.",
}

TAG_LIST_EXAMPLE = [
    {
        "id": UUID_EXAMPLE,
        "name": "technology",
    },
    {
        "id": UUID_EXAMPLE,
        "name": "python",
    },
]


ACCEPT_GUIDELINES_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=ContributorOnboardingSerializer,
        description="Guidelines retrieved successfully",
        examples=[
            OpenApiExample(
                name="Already a contributor",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Already a contributor",
                },
            ),
        ],
    ),
    201: OpenApiResponse(
        response=ContributorOnboardingSerializer,
        description="Guidelines retrieved successfully",
        examples=[
            OpenApiExample(
                name="Onboarding successful",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Congratulations! You are now a Tech Hive contributor!",
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    400: ErrorDataResponseSerializer,
    422: OpenApiResponse(
        response=ErrorDataResponseSerializer,
        description="Validation Error",
    ),
}

CATEGORY_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=CategorySerializer,
        description="Categories Fetched",
        examples=[
            OpenApiExample(
                name="Categories Fetched",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Categories retrieved successfully.",
                    "data": CATEGORY_LIST_EXAMPLE,
                },
            ),
        ],
    ),
}

TAG_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=TagSerializer,
        description="Tags Fetched",
        examples=[
            OpenApiExample(
                name="Tags Fetched",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Tags retrieved successfully.",
                    "data": TAG_LIST_EXAMPLE,
                },
            ),
        ],
    ),
}

ARTICLE_LIST_RESPONSE_EXAMPLE = {}
