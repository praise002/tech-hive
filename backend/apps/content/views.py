from apps.common.pagination import DefaultPagination
from apps.common.responses import CustomResponse
from apps.content.models import Article, Category, Tag
from apps.content.schema_examples import CATEGORY_RESPONSE_EXAMPLE, TAG_RESPONSE_EXAMPLE
from apps.content.serializers import (
    ArticleCreateDraftSerializer,
    ArticleSerializer,
    CategorySerializer,
    TagSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

category_tags = ["Categories"]
article_tags = ["Articles"]


class CategoryGenericView(ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = DefaultPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ["name"]
    ordering_fields = ["name"]  # TODO: Add by popularity later
    # ordering = ["name"] # might not need use tyhe model default ordering
    queryset = Category.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data)
            return CustomResponse.success(
                message="Categories retrieved successfully.",
                data=paginated_data.data,
                status_code=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message="Categories retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="List all categories",
        description="Retrieve a list of all blog categories. Categories are broad groupings used to organize articles and help users browse content by topic.",
        tags=category_tags,
        responses=CATEGORY_RESPONSE_EXAMPLE,
        auth=[],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# TODO: RETURN ARTICLE WITH IT'S TAGS,
# TODO: FOR POST, IT CONVERTS THE TAGS TO LOWERCASE THEN POST IT


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


# Article Management Endpoints
class ArticleGenericView(ListCreateAPIView):
    # List published article
    queryset = Article.published.select_related("category", "author").all()
    serializer_class = ArticleSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["title", "content"]
    pagination_class = DefaultPagination
    
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return ArticleCreateDraftSerializer
        return ArticleSerializer

    @extend_schema(
        summary="Retrieve a list of articles",
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

    # Create new draft
    def post(self, request):
        pass

    def patch(self, request):
        pass


class ArticleRetrieveView(APIView):
    # Published article, owner/staff - unpublished(draft)
    # /api/articles/{id}/
    def get(self, request):
        pass


class ArticleSubmitView(APIView):
    # /api/articles/{id}/submit/ - is it restful?
    # Submit draft for review - owner
    def post(self, request):
        pass


class ArticleWithdrawView(APIView):
    # /api/articles/{id}/withdraw/ - is it restful?
    # Withdraw from review - owner
    def post(self, request):
        pass


class ArticlePublishView(APIView):
    # /api/articles/{id}/publish/ - is it restful?
    # Publish article - Editor/Manager
    def post(self, request):
        pass


class ArticlePublishView(APIView):
    # /api/articles/{id}/archive/ - is it restful?
    # Archive article -	Manager/Owner of article
    def post(self, request):
        pass


# Review Workflow Endpoints
class ArticleRequestChangesView(APIView):
    # /api/articles/{id}/request-changes/ - is it restful?
    # Request revisions - Reviewer
    def post(self, request):
        pass


class ArticleApproveToEditView(APIView):
    # /api/articles/{id}/approve/ - is it restful?
    # Approve for publishing - Reviewer
    def post(self, request):
        pass


# /api/articles/{id}/comments/	GET	List comments	Participant
# /api/articles/{id}/comments/	POST	Add comment	Reviewer/Editor/Manager


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
