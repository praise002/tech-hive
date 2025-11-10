from apps.accounts.schema_examples import UNAUTHORIZED_USER_RESPONSE
from apps.common.errors import ErrorCode
from apps.common.schema_examples import (
    AVATAR_URL,
    DATETIME_EXAMPLE,
    EMAIL_EXAMPLE,
    ERR_RESPONSE_STATUS,
    SUCCESS_RESPONSE_STATUS,
    UUID_EXAMPLE,
)
from apps.common.serializers import ErrorDataResponseSerializer, ErrorResponseSerializer
from apps.content.serializers import (
    ArticleSerializer,
    CommentSerializer,
    SavedArticleSerializer,
)
from apps.profiles.serializers import UserSerializer
from drf_spectacular.utils import OpenApiExample, OpenApiResponse

TAGS = [
    {"id": "a4abfe0b-5466-46ab-8dbe-b469133aaede", "name": "django"},
    {"id": "d5afcd69-4c7d-4ea5-94bd-e1a2549a3f72", "name": "python"},
]

ARTICLE_1 = {
    "id": "54a05aa7-a299-48c5-8076-ec6e8134b888",
    "title": "Test 1",
    "slug": "test-1",
    "content": "Test content",
    "cover_image_url": "",
    "read_time": 5,
    "status": "draft",
    "created_at": "2025-08-31T22:11:49.564213Z",
    "is_featured": False,
    "author": "Eki Benson",
    "total_reaction_counts": 0,
    "reaction_counts": {},
    "tags": TAGS,
}

ARTICLE_UPDATED = {"title": "Test post", "content": "Test content updated"}

PROFILE_EXAMPLE = {
    "id": UUID_EXAMPLE,
    "first_name": "Bob",
    "last_name": "Joe",
    "username": "bob-joe",
    "email": EMAIL_EXAMPLE,
    "created_at": DATETIME_EXAMPLE,
    "avatar_url": AVATAR_URL,
}


ARTICLES = [
    {
        "id": "54a05aa7-a299-48c5-8076-ec6e8134b888",
        "title": "Test 1",
        "slug": "test-1",
        "content": "Test content",
        "cover_image_url": "",
        "read_time": 5,
        "status": "ready_for_publishing",
        "created_at": "2025-08-31T22:11:49.564213Z",
        "is_featured": False,
        "author": "Eki Benson",
        "total_reaction_counts": 0,
        "reaction_counts": {},
        "tags": TAGS,
    },
    {
        "id": "146541be-1b9b-48a2-8117-2b5fd4bd301b",
        "title": "Test title 2",
        "slug": "test-title-2",
        "content": "Test content",
        "cover_image_url": "",
        "read_time": 0,
        "status": "published",
        "created_at": "2025-08-12T10:00:54.576519Z",
        "is_featured": False,
        "author": "Praise Idowu",
        "total_reaction_counts": 2,
        "reaction_counts": {"❤️": 2},
        "tags": [{"id": "d5afcd69-4c7d-4ea5-94bd-e1a2549a3f72", "name": "python"}],
    },
    {
        "id": "26b0dee3-54a8-46eb-8c9d-00ca481d201f",
        "title": "Test title",
        "slug": "test-title",
        "content": "Test content",
        "cover_image_url": "",
        "read_time": 5,
        "status": "published",
        "created_at": "2025-08-07T18:48:26.389204Z",
        "is_featured": False,
        "author": "Praise Idowu",
        "total_reaction_counts": 4,
        "reaction_counts": {"❤️": 1, "👍": 1, "🔥": 1, "😍": 1},
        "tags": [{"id": "d5afcd69-4c7d-4ea5-94bd-e1a2549a3f72", "name": "python"}],
    },
]

DRAFTS_ARTICLES = [
    {
        "id": "54a05aa7-a299-48c5-8076-ec6e8134b888",
        "title": "My Draft Article",
        "slug": "my-draft-article",
        "content": "This is a draft article content",
        "cover_image_url": "",
        "read_time": 3,
        "status": "draft",
        "created_at": "2025-09-01T10:30:00.000000Z",
        "is_featured": False,
        "author": "John Doe",
        "total_reaction_counts": 0,
        "reaction_counts": {},
        "tags": [{"id": "a4abfe0b-5466-46ab-8dbe-b469133aaede", "name": "django"}],
    }
]

PUBLISHED_ARTICLES = [
    {
        "id": "146541be-1b9b-48a2-8117-2b5fd4bd301b",
        "title": "Test title 2",
        "slug": "test-title-2",
        "content": "Test content",
        "cover_image_url": "",
        "read_time": 5,
        "status": "published",
        "created_at": "2025-08-12T10:00:54.576519Z",
        "is_featured": False,
        "author": "Praise Idowu",
        "total_reaction_counts": 2,
        "reaction_counts": {"❤️": 2},
        "tags": [{"id": "d5afcd69-4c7d-4ea5-94bd-e1a2549a3f72", "name": "python"}],
    }
]

SUBMITTED_ARTICLES = [
    {
        "id": "7f8e9d6c-5b4a-3928-1765-4c3b2a1f0e9d",
        "title": "Article Under Review",
        "slug": "article-under-review",
        "content": "This article is currently being reviewed",
        "cover_image_url": "",
        "read_time": 7,
        "status": "under_review",
        "created_at": "2025-08-30T14:22:33.123456Z",
        "is_featured": False,
        "author": "Jane Smith",
        "total_reaction_counts": 0,
        "reaction_counts": {},
        "tags": [
            {
                "id": "a4abfe0b-5466-46ab-8dbe-b469133aaede",
                "name": "django",
            },
            {
                "id": "d5afcd69-4c7d-4ea5-94bd-e1a2549a3f72",
                "name": "python",
            },
        ],
    },
    {
        "id": "9a8b7c6d-5e4f-3210-9876-5432109876ab",
        "title": "Article Needs Changes",
        "slug": "article-needs-changes",
        "content": "This article needs some changes based on reviewer feedback",
        "cover_image_url": "",
        "read_time": 4,
        "status": "changes_requested",
        "created_at": "2025-08-28T09:15:42.987654Z",
        "is_featured": False,
        "author": "Bob Wilson",
        "total_reaction_counts": 0,
        "reaction_counts": {},
        "tags": [
            {
                "id": "d5afcd69-4c7d-4ea5-94bd-e1a2549a3f72",
                "name": "python",
            }
        ],
    },
]


COMMENTS_DATA_EXAMPLE = {
    "count": 0,
    "next": None,
    "previous": None,
    "results": [
        {
            "id": "9217d492-ec33-4e05-af2c-62aa220b4c51",
            "user_id": "63edac98-9f67-4afb-a944-aa3cb69c580b",
            "article_id": "146541be-1b9b-48a2-8117-2b5fd4bd301b",
            "article_title": "Test title 2",
            "created_at": "2025-08-12T10:00:54.576519Z",
            "is_reply": False,
            "reply_count": 1,
            "body": "portfolio",
        },
        {
            "id": "1e3c03a8-9535-40d7-98e4-30db724a0abb",
            "user_id": "63edac98-9f67-4afb-a944-aa3cb69c580b",
            "article_id": "146541be-1b9b-48a2-8117-2b5fd4bd301b",
            "article_title": "Test title 2",
            "created_at": "2025-08-12T10:00:54.576519Z",
            "is_reply": False,
            "reply_count": 0,
            "body": "Lorem",
        },
        {
            "id": "353949d0-2738-4eb7-a411-e70d8026915d",
            "user_id": "63edac98-9f67-4afb-a944-aa3cb69c580b",
            "article_id": "146541be-1b9b-48a2-8117-2b5fd4bd301b",
            "article_title": "Test title 2",
            "created_at": "2025-08-12T10:00:54.576519Z",
            "is_reply": True,
            "reply_count": 0,
            "body": "Ikr",
        },
    ],
}

SAVED_ARTICLE_EXAMPLE = [
    {
        "id": "8650da13-0443-468f-916e-f0387f98429f",
        "article": {
            "id": "26b0dee3-54a8-46eb-8c9d-00ca481d201f",
            "title": "Test title",
            "slug": "test-title",
            "content": "Test content",
            "cover_image_url": "",
            "read_time": 5,
            "status": "published",
            "created_at": "2025-08-07T18:48:26.389204Z",
            "is_featured": False,
            "author": "Praise Idowu",
            "total_reaction_counts": 4,
            "reaction_counts": {"❤️": 1, "👍": 1, "🔥": 1, "😍": 1},
            "tags": [{"id": "d5afcd69-4c7d-4ea5-94bd-e1a2549a3f72", "name": "python"}],
        },
    },
    {
        "id": "12850bd5-04a8-41f8-87df-68fd34f61b24",
        "article": {
            "id": "146541be-1b9b-48a2-8117-2b5fd4bd301b",
            "title": "Test title 2",
            "slug": "test-title-2",
            "content": "Test content",
            "cover_image_url": "",
            "read_time": 0,
            "status": "published",
            "created_at": "2025-08-12T10:00:54.576519Z",
            "is_featured": False,
            "author": "Praise Idowu",
            "total_reaction_counts": 2,
            "reaction_counts": {"❤️": 2},
            "tags": [{"id": "d5afcd69-4c7d-4ea5-94bd-e1a2549a3f72", "name": "python"}],
        },
    },
]

ARTICLE_CREATE_EXAMPLE = [
    {
        "title": "Test title",
        "content": "Test content",
        "url": "",  # TODO: UPDATE LATER
    }
]


PROFILE_UPDATE_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=UserSerializer,
        description="Profile Update Successful",
        examples=[
            OpenApiExample(
                name="Profile Update Successful",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Profile updated successfully.",
                    "data": PROFILE_EXAMPLE,
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    422: ErrorDataResponseSerializer,
}

PROFILE_RETRIEVE_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Profile Retrieve Successful",
        response=UserSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Profile retrieved successfully.",
                    "data": PROFILE_EXAMPLE,
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
}

PROFILE_DETAIL_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Profile Retrieve Successful",
        response=UserSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Profile retrieved successfully.",
                    "data": PROFILE_EXAMPLE,
                },
            ),
        ],
    ),
    404: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Profile not found",
        examples=[
            OpenApiExample(
                name="Profile not found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "User profile not found.",
                    "code": ErrorCode.NON_EXISTENT,
                },
            ),
        ],
    ),
}

AVATAR_UPDATE_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Avatar Update Successful",
        response=UserSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Profile avatar updated successfully.",
                    "data": {
                        "avatar_url": AVATAR_URL,
                    },
                },
            ),
        ],
    ),
    422: ErrorDataResponseSerializer,
    401: UNAUTHORIZED_USER_RESPONSE,
}

ARTICLE_LIST_EXAMPLE = {
    200: OpenApiResponse(
        description="Articles Fetched",
        response=ArticleSerializer,
        examples=[
            OpenApiExample(
                name="All Articles (No Filter)",
                summary="Default response with all user articles",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Articles retrieved successfully.",
                    "data": ARTICLES,
                },
            ),
            OpenApiExample(
                name="Draft Articles Only",
                summary="Filtered by status=draft",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Articles retrieved successfully.",
                    "data": DRAFTS_ARTICLES,
                },
            ),
            OpenApiExample(
                name="Published Articles Only",
                summary="Filtered by status=published",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Articles retrieved successfully.",
                    "data": PUBLISHED_ARTICLES,
                },
            ),
            OpenApiExample(
                name="Submitted Articles (Multiple Statuses)",
                summary="Articles in submission process (submitted_for_review, under_review, changes_requested)",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Articles retrieved successfully.",
                    "data": SUBMITTED_ARTICLES,
                },
            ),
            OpenApiExample(
                name="Empty Results",
                summary="No articles found matching the filter criteria",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Articles retrieved successfully.",
                    "data": [],
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    403: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Permission Denied",
    ),
}

ARTICLE_CREATE_RESPONSE_EXAMPLE = {
    201: OpenApiResponse(
        description="Article Creation Successful",
        response=UserSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Article created successfully.",
                    "data": ARTICLE_CREATE_EXAMPLE,
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    403: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Permission Denied",
    ),
}

ARTICLE_DETAIL_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Article Retrieval Successful",
        response=UserSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Article detail retrieved successfull.",
                    "data": ARTICLE_1,
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    403: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Permission Denied",
    ),
    404: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Article not found",
        examples=[
            OpenApiExample(
                name="Article not found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Article not found.",
                    "code": ErrorCode.NON_EXISTENT,
                },
            ),
        ],
    ),
}

ARTICLE_UPDATE_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Article Retrieval Successful",
        response=UserSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Article updated successfully.",
                    "data": ARTICLE_UPDATED,
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    403: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Permission Denied",
    ),
}


SAVED_ARTICLES_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Saved articles retrieved successfully",
        response=SavedArticleSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Saved Articles retrieved successfully",
                    "data": SAVED_ARTICLE_EXAMPLE,
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
}


SAVED_ARTICLES_CREATE_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Toggle save status for an article",
        response=SavedArticleSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Article unsaved successfully",
                },
            ),
        ],
    ),
    201: OpenApiResponse(
        description="Toggle save status for an article",
        response=SavedArticleSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Article saved successfully",
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    403: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Permission Denied",
    ),
    422: ErrorDataResponseSerializer,
}

COMMENTS_ARTICLES_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Comments retrieved successfully",
        response=CommentSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Comments retrieved successfully.",
                    "data": COMMENTS_DATA_EXAMPLE,
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
}


USERNAMES_DATA_EXAMPLE = {
    "count": 5,
    "next": None,
    "previous": None,
    "results": [
        {
            "id": "63edac98-9f67-4afb-a944-aa3cb69c580b",
            "username": "john-doe",
        },
        {
            "id": "8f7e6d5c-4b3a-2918-7654-3c2b1a0f9e8d",
            "username": "jane-smith",
        },
        {
            "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "username": "bob-wilson",
        },
        {
            "id": "9876fedc-ba98-7654-3210-fedcba987654",
            "username": "alice-johnson",
        },
        {
            "id": "11223344-5566-7788-99aa-bbccddeeff00",
            "username": "mike-brown",
        },
    ],
}

USERNAMES_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Usernames retrieved successfully",
        response=UserSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Usernames retrieved successfully.",
                    "data": USERNAMES_DATA_EXAMPLE,
                },
            ),
        ],
    ),
}


def build_avatar_request_schema():
    return {
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "avatar": {
                    "type": "string",
                    "format": "binary",
                    "description": "Profile image file",
                },
            },
            "required": ["avatar"],
        }
    }
