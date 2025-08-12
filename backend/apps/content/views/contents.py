from apps.content.schema_examples import CATEGORY_RESPONSE_EXAMPLE, TAG_RESPONSE_EXAMPLE
from apps.content.serializers import (
    
    
    CategorySerializer,
    
)
from apps.common.pagination import DefaultPagination
from rest_framework.generics import ListAPIView

from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.common.responses import CustomResponse
from apps.content.models import Category
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

category_tags = ["Categories"]

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


