from apps.common.responses import CustomResponse
from apps.content.filters import TagFilter
from rest_framework.filters import OrderingFilter

from apps.content.schema_examples import CATEGORY_RESPONSE_EXAMPLE, TAG_RESPONSE_EXAMPLE
from apps.content.serializers import CategorySerializer, TagSerializer
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from apps.common.pagination import DefaultPagination
from apps.content.models import Category, Tag

category_tags = ["Categories"]
article_tags = ["Articles"]


class CategoryGenericView(ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = DefaultPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ["name"]
    ordering_fields = ["name"]    # TODO: Add by popularity later
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


class TagGenericView(ListAPIView):
    serializer_class = TagSerializer
    filterset_class = TagFilter
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["name"]
    queryset = Tag.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        limit = int(request.query_params.get("limit", 10))
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
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, reequest):
        # get_or_create
        pass


class ArticleView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass

    def patch(self, request):
        pass
