from apps.accounts.schema_examples import UNAUTHORIZED_USER_RESPONSE
from apps.common.schema_examples import SUCCESS_RESPONSE_STATUS, UUID_EXAMPLE
from apps.common.serializers import ErrorDataResponseSerializer
from apps.content.serializers import (
    ArticleSerializer,
    CategorySerializer,
    ContributorOnboardingSerializer,
    EventSerializer,
    JobSerializer,
    ResourceSerializer,
    TagSerializer,
    ToolSerializer,
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
        "reaction_counts": {"❤️": 1, "👍": 1, "🔥": 1, "😍": 1},
        "tags": [{"id": "d5afcd69-4c7d-4ea5-94bd-e1a2549a3f72", "name": "python"}],
    },
]

ARTICLE_DETAIL_EXAMPLE = {
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

ARTICLE_LIST_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Articles Fetched",
        response=ArticleSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Articles retrieved successfully.",
                    "data": ARTICLES,
                },
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
}

EVENTS_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        description="Events retrieved successfully",
        response=EventSerializer,
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Events retrieved successfully.",
                    "data": EVENTS_DATA_EXAMPLE,
                },
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
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Resources retrieved successfully.",
                    "data": RESOURCES_DATA_EXAMPLE,
                },
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
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Tools retrieved successfully.",
                    "data": TOOLS_DATA_EXAMPLE,
                },
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
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Jobs retrieved successfully.",
                    "data": JOBS_DATA_EXAMPLE,
                },
            ),
        ],
    ),
}
