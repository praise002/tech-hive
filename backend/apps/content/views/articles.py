import logging

from apps.accounts.utils import UserRoles
from apps.common.pagination import DefaultPagination
from apps.common.responses import CustomResponse
from apps.content.models import Article, Tag
from apps.content.schema_examples import (
    ACCEPT_GUIDELINES_RESPONSE_EXAMPLE,
    TAG_RESPONSE_EXAMPLE,
)
from apps.content.serializers import (
    ArticleSerializer,
    ContributorOnboardingSerializer,
    TagSerializer,
)
from django.contrib.auth.models import Group
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

article_tags = ["Articles"]
onboarding_tags = ["Onboarding"]

logger = logging.getLogger(__name__)
security_logger = logging.getLogger("security")


class AcceptGuidelinesView(APIView):
    """
    Accept contributor guidelines and become a contributor.

    Processes guideline acceptance and assigns contributor role to the user.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ContributorOnboardingSerializer

    @extend_schema(
        summary="Accept contributor guidelines",
        description="Accept contributor guidelines and terms to become a contributor. "
        "This endpoint processes acceptance, and assigns contributor role.",
        tags=onboarding_tags,
        responses=ACCEPT_GUIDELINES_RESPONSE_EXAMPLE,
    )
    def post(self, request):
        if request.user.groups.filter(name=UserRoles.CONTRIBUTOR).exists():
            return CustomResponse.success(message="Already a contributor")

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            serializer.save()

            contributor_group, _ = Group.objects.get_or_create(
                name=UserRoles.CONTRIBUTOR
            )
            request.user.groups.add(contributor_group)
            logger.info(f"User {request.user.id} became contributor")

        return CustomResponse.success(
            message="Congratulations! You are now a Tech Hive contributor!",
            status_code=status.HTTP_201_CREATED,
        )


# Drafts - never submitted, just in draft
# submitted for review, under review, changes requested, rejected - submitted articles - users can edit it
# if it is marked as changes requested
# published - under published article section - paginate
# GET /articles/ → public published articles (all authors)
# GET /articles/?status=draft → authenticated user's drafts
# GET /users/{username}/articles/ → specific user's published articles (profile view)


class ArticleRetrieveUpdateView(RetrieveUpdateAPIView):  # USE APIView
    pass


class ArticleListView(ListCreateAPIView):
    # List all published article
    queryset = Article.published.select_related("category", "author").all()
    serializer_class = ArticleSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["title", "content"]
    pagination_class = DefaultPagination

    @extend_schema(
        summary="Retrieve a list of all published articles",
        description="This endpoint allows.",
        parameters=[
            OpenApiParameter(
                name="search",
                description="Search across title, and description.",
            ),
        ],
        tags=article_tags,
        auth=[],
        # responses=ARTICLE_LIST_RESPONSE_EXAMPLE,
    )
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve profiles with pagination, search, and filtering.
        """
        return super().get(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data)
            return CustomResponse.success(
                message="Articles retrieved successfully.",
                data=paginated_data.data,
                status_code=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message="Articles retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class TagGenericView(ListAPIView):
    serializer_class = TagSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["name"]
    queryset = Tag.objects.all()
    default_limit = 10

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        try:
            limit = int(request.query_params.get("limit", self.default_limit))
        except ValueError:
            # TODO: TEST IT: if an invalid integer uses the default instead of crashing
            limit = self.default_limit

        queryset = queryset[:limit]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data)
            return CustomResponse.success(
                message="Tags retrieved successfully.",
                data=paginated_data.data,
                status_code=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message="Tags retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="List all tags",
        description="Retrieve a list of all tags. Tags are keywords or labels that help categorize and organize articles, making it easier for users to find content related to specific topics.",
        tags=article_tags,
        responses=TAG_RESPONSE_EXAMPLE,
        auth=[],
        parameters=[
            OpenApiParameter(
                name="limit",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Maximum number of tags to return (default is 10).",
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TagRemoveView(APIView):
    pass


# Do for every content
class RSSFeedInfoView(APIView):
    @extend_schema(
        summary="RSS Feed Information",
        description="Get information about subscribing to Tech Hive's RSS feed.",
        tags=article_tags,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "rss_url": {"type": "string"},
                    "description": {"type": "string"},
                    "items_count": {"type": "integer"},
                },
            }
        },
    )
    def get(self, request):
        base_url = request.build_absolute_uri("/").rstrip("/")
        return CustomResponse.success(
            message="Tags retrieved successfully.",
            data={
                "rss_url": f"{base_url}/api/v1/articles/feed/",
                "description": "Subscribe to get the latest Tech Hive articles",
                "format": "RSS 2.0 XML",
                "items_count": 10,
                "update_frequency": "When new articles are published",
            },
            status_code=status.HTTP_200_OK,
        )
