from apps.accounts.schema_examples import UNAUTHORIZED_USER_RESPONSE
from apps.common.errors import ErrorCode
from apps.common.schema_examples import (
    AVATAR_URL,
    COVER_IMAGE_URL,
    ERR_RESPONSE_STATUS,
    SUCCESS_RESPONSE_STATUS,
    UUID_EXAMPLE,
)
from apps.common.serializers import (
    ErrorDataResponseSerializer,
    ErrorResponseSerializer,
    SuccessResponseSerializer,
)
from apps.content.serializers import (
    ArticleEditorSerializer,
    ArticleReactionStatusSerializer,
    ArticleSerializer,
    ArticleSubmitResponseSerializer,
    ArticleSummaryResponseSerializer,
    CategorySerializer,
    CommentLikeSerializer,
    CommentLikeStatusSerializer,
    CommentResponseSerializer,
    ContributorOnboardingSerializer,
    CoverImageSerializer,
    EventSerializer,
    JobSerializer,
    ResourceSerializer,
    ReviewStartResponseSerializer,
    TagSerializer,
    ThreadReplySerializer,
    ToolSerializer,
    UserMentionSerializer,
)
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


ARTICLES = [
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
        "reaction_counts": {"❤️": 4, "👍": 1, "🔥": 1, "😍": 3},
        "tags": [{"id": "d5afcd69-4c7d-4ea5-94bd-e1a2549a3f72", "name": "python"}],
    },
]


ARTICLE_DETAIL_EXAMPLE = {
    "id": "09fc9e71-d071-4fb4-ba28-16a493e609d6",
    "title": "Test Article",
    "slug": "test-article",
    "content": "<p>Test purposes</p>",
    "cover_image_url": COVER_IMAGE_URL,
    "read_time": 1,
    "status": "published",
    "created_at": "2025-10-27T00:48:44.637026Z",
    "is_featured": False,
    "author": "Praise ID",
    "total_reaction_counts": 0,
    "reaction_counts": {},
    "tags": [],
    "comments": [
        {
            "id": "8485b084-2257-48a1-82bf-cffa90373a80",
            "thread_id": "6dd9d3f8-bdd3-43e8-83f9-a5533349f776",
            "body": "This is cool",
            "created_at": "2025-10-27T18:03:01.913900Z",
            "user_name": "Praise ID",
            "user_username": "praise-id",
            "user_avatar": AVATAR_URL,
            "total_replies": 0,
        }
    ],
    "comments_count": 1,
}

EVENT_EXAMPLE = {
    "id": "d9c34a1a-9b2b-4a0a-8b1a-1b9b4a0a8b1a",
    "title": "Tech Conference 2025",
    "desc": "Join us for the premier tech conference of the year!",
    "start_date": "2025-11-15T09:00:00Z",
    "end_date": "2025-11-17T17:00:00Z",
    "location": "San Francisco, CA",
    "agenda": "Keynotes, workshops, and networking events",
    "ticket_url": "https://example.com/tech-conference-2025",
    "category": "Conference",
}

EVENTS_DATA_EXAMPLE = {
    "count": 1,
    "next": None,
    "previous": None,
    "results": [EVENT_EXAMPLE],
}

RESOURCE_EXAMPLE = {
    "id": "f8e7c6b5-4a3f-4c2e-9b8f-7a6d5e4c3b2a",
    "name": "Awesome Django Tutorial",
    "image_url": "https://example.com/django-tutorial.png",
    "body": "A comprehensive guide to building web apps with Django",
    "url": "https://example.com/django-tutorial",
    "category": "Tutorial",
}

RESOURCES_DATA_EXAMPLE = {
    "count": 1,
    "next": None,
    "previous": None,
    "results": [RESOURCE_EXAMPLE],
}

TOOL_TAG_EXAMPLE = {"id": "b1d6e859-df99-4842-b1d6-e859df99bc93", "name": "AI"}

TOOL_EXAMPLE = {
    "id": "a7b8c9d0-1a2b-4c5d-8e9f-0a1b2c3d4e5f",
    "name": "AI Tool",
    "desc": "An AI-powered tool for content creation",
    "url": "https://example.com/ai-tool",
    "image_url": "https://example.com/ai-tool.png",
    "call_to_action": "Try it now!",
    "tags": [TOOL_TAG_EXAMPLE],
    "category": "AI",
}

TOOLS_DATA_EXAMPLE = {
    "count": 1,
    "next": None,
    "previous": None,
    "results": [TOOL_EXAMPLE],
}

JOB_EXAMPLE = {
    "id": "2c9e2a3b-f7a8-4a9b-b3a1-d7c8e9f0a1b2",
    "title": "Software Engineer",
    "company": "TechHive Inc.",
    "desc": "We are looking for a talented software engineer to join our team.",
    "requirements": "Bachelor's degree in Computer Science, 3+ years of experience",
    "responsibilities": "Develop and maintain web applications",
    "url": "https://example.com/jobs/software-engineer",
    "salary": "80000-120000",
    "location": "San Francisco, CA",
    "job_type": "Full-time",
    "work_mode": "Remote",
    "category": "Engineering",
}

JOBS_DATA_EXAMPLE = {
    "count": 1,
    "next": None,
    "previous": None,
    "results": [JOB_EXAMPLE],
}

REPLIES_DATA_EXAMPLE = [
    {
        "id": UUID_EXAMPLE,
        "body": "Great article!",
        "created_at": "2025-10-27T10:00:00Z",
        "user_name": "John Doe",
        "user_username": "john-doe",
        "user_avatar": AVATAR_URL,
        "replying_to_name": "Joseph Ayo",
        "replying_to_username": "josedev",
    },
    {
        "id": UUID_EXAMPLE,
        "body": "I agree with you",
        "created_at": "2025-10-27T10:05:00Z",
        "user_name": "Jane Smith",
        "user_username": "jane-smith",
        "user_avatar": AVATAR_URL,
        "replying_to_name": "Joseph Ayo",
        "replying_to_username": "josedev",
    },
]

COMMENT_CREATE_EXAMPLE = {
    "id": UUID_EXAMPLE,
    "thread_id": "2c9e2a3b-f7a8-4a9b-b3a1-d7c8e9f0a1b2",
    "body": "I agree with this point!",
    "created_at": "2025-10-27T10:05:00Z",
    "user_name": "Jane Smith",
    "user_username": "jane-smith",
    "user_avatar": AVATAR_URL,
    "is_root": False,
}

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
                value=CATEGORY_LIST_EXAMPLE,
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

RSS_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=SuccessResponseSerializer,
        description="RSS Feed Fetched",
        examples=[
            OpenApiExample(
                name="RSS Feed Fetched",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "RSS Feed information retrieved successfully.",
                    "data": {
                        "rss_url": "https://127.0.0.1:8000/api/v1/articles/feed/",
                        "description": "Subscribe to get the latest Tech Hive articles",
                        "format": "RSS 2.0 XML",
                        "items_count": 10,
                        "update_frequency": "When new articles are published",
                    },
                },
            ),
        ],
    ),
}


ARTICLE_LIST_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Articles Fetched",
        response=ArticleSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value=ARTICLES,
            ),
        ],
    ),
}

ARTICLE_DETAIL_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Article Retrieval Successful",
        response=ArticleSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Article detail retrieved successfully.",
                    "data": ARTICLE_DETAIL_EXAMPLE,
                },
            ),
        ],
    ),
    404: OpenApiResponse(
        description="Article not found",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Article Not Found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Article not found.",
                    "code": ErrorCode.NON_EXISTENT,
                },
            ),
        ],
    ),
}

EVENTS_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Events retrieved successfully",
        response=EventSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value=[EVENT_EXAMPLE],
            ),
        ],
    ),
}

RESOURCES_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Resources retrieved successfully",
        response=ResourceSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value=[RESOURCE_EXAMPLE],
            ),
        ],
    ),
}

TOOLS_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Tools retrieved successfully",
        response=ToolSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value=[TOOL_EXAMPLE],
            ),
        ],
    ),
}

JOB_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Jobs retrieved successfully",
        response=JobSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value=[JOB_EXAMPLE],
            ),
        ],
    ),
}

THREAD_REPLIES_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Replies retrieved successfully",
        response=ThreadReplySerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Replies retrieved successfully.",
                    "data": REPLIES_DATA_EXAMPLE,
                },
            ),
        ],
    ),
    404: OpenApiResponse(
        description="Comment not found",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Comment Not Found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Comment not found",
                    "code": ErrorCode.NON_EXISTENT,
                },
            ),
        ],
    ),
    422: ErrorDataResponseSerializer,
}

COMMENT_CREATE_RESPONSE_EXAMPLE = {
    201: OpenApiResponse(
        description="Comment created successfully",
        response=CommentResponseSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Comment created successfully.",
                    "data": COMMENT_CREATE_EXAMPLE,
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    404: OpenApiResponse(
        description="Article not found",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Article Not Found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Article not found",
                    "code": ErrorCode.NON_EXISTENT,
                },
            ),
        ],
    ),
    422: ErrorDataResponseSerializer,
}


COMMENT_LIKE_TOGGLE_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Like status toggled successfully. The 'action' field indicates whether the comment was 'liked' or 'unliked'.",
        response=CommentLikeSerializer,
        examples=[
            OpenApiExample(
                name="User liked the comment",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Comment liked successfully.",
                    "data": {
                        "is_liked": True,
                        "like_count": 16,
                        "action": "liked",
                    },
                },
            ),
            OpenApiExample(
                name="User unliked the comment",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Comment unliked successfully.",
                    "data": {
                        "is_liked": False,
                        "like_count": 15,
                        "action": "unliked",
                    },
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    404: OpenApiResponse(
        description="Comment not found",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Comment Not Found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Article not found",
                    "code": ErrorCode.NON_EXISTENT,
                },
            ),
        ],
    ),
    422: ErrorDataResponseSerializer,
    503: OpenApiResponse(
        description="Like service unavailable",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Like service unavailable",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Like service temporarily unavailable",
                    "code": ErrorCode.SERVICE_UNAVAILABLE,
                },
            ),
        ],
    ),
}


COMMENT_LIKE_STATUS_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Like status retrieved successfully. `is_liked` will be `null` for unauthenticated users.",
        response=CommentLikeStatusSerializer,
        examples=[
            OpenApiExample(
                name="Authenticated user has liked",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Like status retrieved successfully.",
                    "data": {"like_count": 15, "is_liked": True},
                },
            ),
            OpenApiExample(
                name="Authenticated user has not liked",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Like status retrieved successfully.",
                    "data": {"like_count": 15, "is_liked": False},
                },
            ),
            OpenApiExample(
                name="Unauthenticated user",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Like status retrieved successfully.",
                    "data": {"like_count": 15, "is_liked": None},
                },
            ),
        ],
    ),
    404: OpenApiResponse(
        description="Comment not found",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Comment Not Found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Comment not found",
                    "code": ErrorCode.NON_EXISTENT,
                },
            ),
        ],
    ),
    503: OpenApiResponse(
        description="Like service unavailable",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Like service unavailable",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Like service temporarily unavailable",
                    "code": ErrorCode.SERVICE_UNAVAILABLE,
                },
            ),
        ],
    ),
}


ARTICLE_REACTION_TOGGLE_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=ArticleReactionStatusSerializer,
        description="Reaction toggled successfully. The 'action' field indicates whether the reaction was 'added' or 'removed'.",
        examples=[
            OpenApiExample(
                name="Reaction added",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Reaction added successfully",
                    "data": {
                        "article_id": UUID_EXAMPLE,
                        "reaction_type": "❤️",
                        "action": "added",
                        "is_reacted": True,
                        "reaction_counts": {
                            "❤️": 13,
                            "😍": 8,
                            "👍": 5,
                            "🔥": 3,
                        },
                        "total_reactions": 29,
                    },
                },
            ),
            OpenApiExample(
                name="Reaction removed",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Reaction removed successfully",
                    "data": {
                        "article_id": UUID_EXAMPLE,
                        "reaction_type": "❤️",
                        "action": "removed",
                        "is_reacted": False,
                        "reaction_counts": {
                            "❤️": 12,
                            "😍": 8,
                            "👍": 5,
                            "🔥": 3,
                        },
                        "total_reactions": 28,
                    },
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    403: OpenApiResponse(
        description="Article is not published",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Unpublished Article",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Cannot react to unpublished articles",
                    "code": ErrorCode.FORBIDDEN,
                },
            ),
        ],
    ),
    404: OpenApiResponse(
        description="Article not found",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Article Not Found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Article not found",
                    "code": ErrorCode.NON_EXISTENT,
                },
            ),
        ],
    ),
    422: ErrorDataResponseSerializer,
}


ARTICLE_REACTION_STATUS_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=ArticleReactionStatusSerializer,
        description="Reaction status retrieved successfully. `user_reactions` will be `null` for unauthenticated users.",
        examples=[
            OpenApiExample(
                name="Authenticated user with reactions",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Reaction status retrieved successfully",
                    "data": {
                        "article_id": UUID_EXAMPLE,
                        "reaction_counts": {
                            "❤️": 12,
                            "😍": 8,
                            "👍": 5,
                            "🔥": 3,
                        },
                        "total_reactions": 28,
                        "user_reactions": ["❤️", "👍"],
                    },
                },
            ),
            OpenApiExample(
                name="Authenticated user without reactions",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Reaction status retrieved successfully",
                    "data": {
                        "article_id": UUID_EXAMPLE,
                        "reaction_counts": {
                            "❤️": 12,
                            "😍": 8,
                            "👍": 5,
                            "🔥": 3,
                        },
                        "total_reactions": 28,
                        "user_reactions": [],
                    },
                },
            ),
            OpenApiExample(
                name="Unauthenticated user",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Reaction status retrieved successfully",
                    "data": {
                        "article_id": UUID_EXAMPLE,
                        "reaction_counts": {
                            "❤️": 12,
                            "😍": 8,
                            "👍": 5,
                            "🔥": 3,
                        },
                        "total_reactions": 28,
                        "user_reactions": None,
                    },
                },
            ),
        ],
    ),
    404: OpenApiResponse(
        description="Article not found",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Article Not Found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Article not found",
                    "code": ErrorCode.NON_EXISTENT,
                },
            ),
        ],
    ),
}

ARTICLE_SUMMARY_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Summary generated successfully",
        response=ArticleSummaryResponseSerializer,
        examples=[
            OpenApiExample(
                name="Fresh Summary",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Article summary generated successfully.",
                    "data": {
                        "article_id": UUID_EXAMPLE,
                        "article_title": "Getting Started with Django REST Framework",
                        "article_slug": "getting-started-with-django-rest-framework",
                        "summary": "- Django REST Framework (DRF) is a powerful toolkit for building Web APIs in Django\n- It provides serializers for converting complex data types to native Python datatypes\n- ViewSets and routers enable rapid API development with minimal code\n- Built-in authentication and permissions ensure secure API endpoints\n- The browsable API makes testing and debugging straightforward",
                        "cached": False,
                    },
                },
            ),
            OpenApiExample(
                name="Cached Summary",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Article summary retrieved from cache.",
                    "data": {
                        "article_id": UUID_EXAMPLE,
                        "article_title": "Getting Started with Django REST Framework",
                        "article_slug": "getting-started-with-django-rest-framework",
                        "summary": "- Django REST Framework (DRF) is a powerful toolkit for building Web APIs in Django\n- It provides serializers for converting complex data types to native Python datatypes\n- ViewSets and routers enable rapid API development with minimal code\n- Built-in authentication and permissions ensure secure API endpoints\n- The browsable API makes testing and debugging straightforward",
                        "cached": True,
                    },
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    403: OpenApiResponse(
        description="Article is not published",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Unpublished Article",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Cannot summarize unpublished articles",
                    "code": ErrorCode.FORBIDDEN,
                },
            ),
        ],
    ),
    404: OpenApiResponse(
        description="Article not found",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Article Not Found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Article not found",
                    "code": ErrorCode.NON_EXISTENT,
                },
            ),
        ],
    ),
    422: ErrorDataResponseSerializer,
    429: OpenApiResponse(
        description="Rate limit exceeded",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Rate Limit Exceeded",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Rate limit exceeded.",
                    "code": ErrorCode.RATE_LIMIT_EXCEEDED,
                },
            ),
        ],
    ),
    503: OpenApiResponse(
        description="AI service unavailable",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Service Unavailable",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Summary generation service temporarily unavailable",
                    "code": ErrorCode.SERVICE_UNAVAILABLE,
                },
            ),
        ],
    ),
}


USER_SEARCH_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=UserMentionSerializer(many=True),
        description="Users retrieved successfully",
        examples=[
            OpenApiExample(
                name="Successful search",
                value={
                    "status": "success",
                    "message": "Users retrieved successfully",
                    "data": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "name": "John Doe",
                            "avatar_url": "https://example.com/avatars/john.jpg",
                            "cursor_color": "#FF5733",
                        },
                        {
                            "id": "660e8400-e29b-41d4-a716-446655440001",
                            "name": "Jane Smith",
                            "avatar_url": "https://example.com/avatars/jane.jpg",
                            "cursor_color": "#3357FF",
                        },
                    ],
                },
            ),
            OpenApiExample(
                name="No results found",
                value={
                    "status": "success",
                    "message": "No users found matching your search",
                    "data": [],
                },
            ),
            OpenApiExample(
                name="No users available for article status",
                value={
                    "status": "success",
                    "message": "No users available for mentions in this article status",
                    "data": [],
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    404: OpenApiResponse(
        description="Not found",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Not found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Not found",
                    "error_code": "non_existent",
                },
            )
        ],
    ),
    422: ErrorDataResponseSerializer,
}


USER_BATCH_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=UserMentionSerializer,
        description="Users retrieved successfully",
        examples=[
            OpenApiExample(
                name="Successful batch fetch",
                value={
                    "status": "success",
                    "message": "Users fetched",
                    "data": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "name": "John Doe",
                            "avatar_url": "https://example.com/avatars/john.jpg",
                            "cursor_color": "#FF6B6B",
                        },
                        {
                            "id": "660e8400-e29b-41d4-a716-446655440001",
                            "name": "Jane Smith",
                            "avatar_url": "https://example.com/avatars/jane.jpg",
                            "cursor_color": "#4ECDC4",
                        },
                    ],
                },
                response_only=True,
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    422: ErrorDataResponseSerializer,
}

USER_BATCH_REQUEST_EXAMPLE = [
    OpenApiExample(
        name="Batch request",
        value={
            "user_ids": [
                "550e8400-e29b-41d4-a716-446655440000",
                "660e8400-e29b-41d4-a716-446655440001",
            ]
        },
        request_only=True,
    ),
]

COVER_IMAGE_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Cover image uploaded successfully",
        response=CoverImageSerializer,
        examples=[
            OpenApiExample(
                name="Success",
                value={
                    "status": "success",
                    "message": "Cover image uploaded successfully",
                    "data": {
                        "cover_image_url": "https://example.com/media/covers/article-123.jpg"
                    },
                },
            )
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    403: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Permission Denied",
    ),
    422: ErrorDataResponseSerializer,
}


ARTICLE_EDITOR_RESPONSE_EXAMPLE = {
    200: ArticleEditorSerializer,
    401: UNAUTHORIZED_USER_RESPONSE,
    403: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Permission Denied",
    ),
    404: OpenApiResponse(
        description="Article not found",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Article Not Found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Article not found.",
                    "code": ErrorCode.NON_EXISTENT,
                },
            ),
        ],
    ),
}


ARTICLE_EDITOR_EXAMPLE = [
    OpenApiExample(
        name="Success - Draft Article",
        value={
            "status": "success",
            "message": "Article loaded successfully",
            "data": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "category": None,
                "title": "Getting Started with Django REST Framework",
                "slug": "getting-started-with-django-rest-framework",
                "content": "<p>Django REST Framework is a powerful toolkit...</p>",
                "cover_image_url": None,
                "status": "draft",
                "liveblocks_room_id": "article-550e8400-e29b-41d4-a716-446655440000",
                "user_can_edit": True,
                "is_published": False,
                "author": {
                    "id": "660e8400-e29b-41d4-a716-446655440001",
                    "name": "John Doe",
                    "avatar_url": AVATAR_URL,
                },
                "assigned_reviewer": None,
                "assigned_editor": None,
                "tags": [],
                "created_at": "2025-12-28T10:00:00Z",
                "content_last_synced_at": None,
                "updated_at": "2025-12-28T10:00:00Z",
            },
        },
        response_only=True,
    ),
    OpenApiExample(
        name="Success - Published Article",
        value={
            "status": "success",
            "message": "Article loaded successfully",
            "data": {
                "id": "770e8400-e29b-41d4-a716-446655440002",
                "category": {
                    "id": "880e8400-e29b-41d4-a716-446655440003",
                    "name": "Web Development",
                    "desc": "Articles about web development, frameworks, and best practices",
                    "slug": "web-development",
                },
                "title": "Advanced Django Patterns for Scalable Applications",
                "slug": "advanced-django-patterns-for-scalable-applications",
                "content": "<p>In this comprehensive guide, we'll explore advanced Django patterns...</p>",
                "cover_image_url": COVER_IMAGE_URL,
                "status": "published",
                "liveblocks_room_id": "article-770e8400-e29b-41d4-a716-446655440002",
                "user_can_edit": False,
                "is_published": True,
                "author": {
                    "id": "660e8400-e29b-41d4-a716-446655440001",
                    "name": "John Doe",
                    "avatar_url": AVATAR_URL,
                },
                "assigned_reviewer": {
                    "id": "990e8400-e29b-41d4-a716-446655440004",
                    "name": "Jane Smith",
                    "avatar_url": "https://example.com/avatars/jane.jpg",
                },
                "assigned_editor": {
                    "id": "aa0e8400-e29b-41d4-a716-446655440005",
                    "name": "Mike Wilson",
                    "avatar_url": "https://example.com/avatars/mike.jpg",
                },
                "tags": [
                    {
                        "id": "bb0e8400-e29b-41d4-a716-446655440006",
                        "name": "django",
                    },
                    {
                        "id": "cc0e8400-e29b-41d4-a716-446655440007",
                        "name": "python",
                    },
                    {
                        "id": "dd0e8400-e29b-41d4-a716-446655440008",
                        "name": "backend",
                    },
                ],
                "created_at": "2025-12-15T09:30:00Z",
                "content_last_synced_at": "2025-12-20T14:45:00Z",
                "updated_at": "2025-12-20T14:45:00Z",
            },
        },
        response_only=True,
    ),
    OpenApiExample(
        name="Info - Published Article Redirect",
        value={
            "status": "info",
            "message": "Article is published. Redirecting to public view.",
            "data": {
                "redirect_url": "/articles/john-doe/advanced-django-patterns-for-scalable-applications"
            },
        },
        response_only=True,
    ),
]


ARTICLE_SUBMIT_RESPONSE_EXAMPLE = {
    201: OpenApiResponse(
        description="Article submitted successfully",
        response=ArticleSubmitResponseSerializer,
        examples=[
            OpenApiExample(
                name="First Submission",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Article submitted for review successfully",
                    "data": {
                        "status": "submitted_for_review",
                        "assigned_reviewer": {
                            "id": UUID_EXAMPLE,
                            "name": "Jane Reviewer",
                            "username": "jane-reviewer",
                            "avatar_url": AVATAR_URL,
                        },
                        "is_resubmission": False,
                    },
                },
            ),
            OpenApiExample(
                name="Resubmission",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Article resubmitted successfully",
                    "data": {
                        "status": "submitted_for_review",
                        "assigned_reviewer": {
                            "id": UUID_EXAMPLE,
                            "name": "Jane Reviewer",
                            "username": "jane-reviewer",
                            "avatar_url": AVATAR_URL,
                        },
                        "is_resubmission": True,
                    },
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
        description="Article not found",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Article Not Found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Article not found",
                    "code": ErrorCode.NON_EXISTENT,
                },
            )
        ],
    ),
    422: ErrorDataResponseSerializer,
    503: OpenApiResponse(
        description="Service unavailable",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Liveblocks Sync Failed",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Editor sync timeout. Please try again.",
                    "code": ErrorCode.SERVICE_UNAVAILABLE,
                },
            ),
            OpenApiExample(
                name="No Reviewers Available",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "No reviewers available. Please contact support.",
                    "code": ErrorCode.SERVICE_UNAVAILABLE,
                },
            ),
        ],
    ),
}


REVIEW_START_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Review started successfully",
        response=ReviewStartResponseSerializer,
        examples=[
            OpenApiExample(
                name="Success",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Review started successfully",
                    "data": {
                        "review_status": "in_progress",
                        "article_status": "under_review",
                        "started_at": "2025-12-29T12:34:56.789Z",
                    },
                },
            ),
        ],
    ),
    401: UNAUTHORIZED_USER_RESPONSE,
    403: OpenApiResponse(
        description="Permission Denied",
        examples=[
            OpenApiExample(
                name="Forbidden",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "You do not have permission to perform this action.",
                    "code": ErrorCode.FORBIDDEN,
                },
            ),
        ],
    ),
    404: OpenApiResponse(
        description="Review not found",
        examples=[
            OpenApiExample(
                name="Review Not Found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Review not found",
                    "code": ErrorCode.NON_EXISTENT,
                },
            ),
        ],
    ),
    422: ErrorDataResponseSerializer,
}

COMMENT_DELETE_RESPONSE_EXAMPLE = {
    204: None,
    401: UNAUTHORIZED_USER_RESPONSE,
    403: OpenApiResponse(
        description="Permission Denied - Only comment author can delete",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Not Comment Author",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "You do not have permission to perform this action.",
                    "code": ErrorCode.FORBIDDEN,
                },
            ),
        ],
    ),
    404: OpenApiResponse(
        description="Comment not found",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Comment Not Found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Comment not found.",
                    "code": ErrorCode.NON_EXISTENT,
                },
            ),
        ],
    ),
}

ASSIGNED_REVIEWS_LIST_RESPONSE_EXAMPLE = {
    401: UNAUTHORIZED_USER_RESPONSE,
    403: OpenApiResponse(
        description="Permission Denied - Only reviewers can access",
        response=ErrorResponseSerializer,
        examples=[
            OpenApiExample(
                name="Not a Reviewer",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "You do not have permission to perform this action.",
                    "code": ErrorCode.FORBIDDEN,
                },
            ),
        ],
    ),
}
