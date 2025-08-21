from apps.accounts.schema_examples import UNAUTHORIZED_USER_RESPONSE
from apps.common.schema_examples import SUCCESS_RESPONSE_STATUS, UUID_EXAMPLE
from apps.content.serializers import CategorySerializer, TagSerializer
from drf_spectacular.utils import OpenApiExample, OpenApiResponse

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

CONTRIBUTOR_GUIDELINES_EXAMPLE = {
    "guidelines": "Welcome to Tech Hive contributor program...",
    "requirements": [
        "Verified email address",
        "Active account",
        "Accept terms and conditions",
    ],
    "user_status": {
        "is_contributor": False,
        "email_verified": True,
        "can_accept": True,
    },
}

CONTRIBUTOR_GUIDELINES_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Guidelines retrieved successfully",
        examples={
            "application/json": {
                "status": "success",
                "message": "Contributor guidelines retrieved successfully",
                "data": CONTRIBUTOR_GUIDELINES_EXAMPLE,
            },
        },
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
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
