from apps.common.pagination import DefaultPagination
from apps.common.responses import CustomResponse
from apps.content.filters import EventFilter, JobFilter
from apps.content.models import Category, Event, Job, Resource, Tool
from apps.content.schema_examples import (
    CATEGORY_RESPONSE_EXAMPLE,
    EVENTS_RESPONSE_EXAMPLE,
    JOB_RESPONSE_EXAMPLE,
    RESOURCES_RESPONSE_EXAMPLE,
    TOOLS_RESPONSE_EXAMPLE,
)
from apps.content.serializers import (
    CategorySerializer,
    EventSerializer,
    JobSerializer,
    ResourceSerializer,
    ToolSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView

tags = ["Contents"]


class CustomListViewSet:
    pass


class CategoryGenericView(ListAPIView):
    serializer_class = CategorySerializer
    pagination_class = DefaultPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ["name"]
    ordering_fields = ["name"]  # TODO: Add by popularity later
    # ordering = ["name"] # might not need use type model default ordering
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
        tags=tags,
        responses=CATEGORY_RESPONSE_EXAMPLE,
        auth=[],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class JobListView(ListAPIView):
    serializer_class = JobSerializer
    pagination_class = DefaultPagination
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    filterset_class = JobFilter
    search_fields = ["title"]

    queryset = Job.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data)
            return CustomResponse.success(
                message="Jobs retrieved successfully.",
                data=paginated_data.data,
                status_code=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message="Jobs retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="List all jobs",
        description="Retrieve a list of all jobs",
        tags=tags,
        responses=JOB_RESPONSE_EXAMPLE,
        auth=[],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EventListView(ListAPIView):
    serializer_class = EventSerializer
    pagination_class = DefaultPagination
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    filterset_class = EventFilter
    search_fields = ["title"]

    queryset = Event.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data)
            return CustomResponse.success(
                message="Events retrieved successfully.",
                data=paginated_data.data,
                status_code=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message="Events retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="List all events",
        description="Retrieve a list of all events",
        tags=tags,
        responses=EVENTS_RESPONSE_EXAMPLE,
        auth=[],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ResourceListView(ListAPIView):
    serializer_class = ResourceSerializer
    pagination_class = DefaultPagination
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    filterset_fields = ["category"]
    search_fields = ["name"]

    queryset = Resource.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data)
            return CustomResponse.success(
                message="Resources retrieved successfully.",
                data=paginated_data.data,
                status_code=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message="Resources retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="List all resources",
        description="Retrieve a list of all resources",
        tags=tags,
        responses=RESOURCES_RESPONSE_EXAMPLE,
        auth=[],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ToolListView(ListAPIView):
    serializer_class = ToolSerializer
    pagination_class = DefaultPagination
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    filterset_fields = ["category"]
    search_fields = ["name"]

    queryset = Tool.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data)
            return CustomResponse.success(
                message="Tools retrieved successfully.",
                data=paginated_data.data,
                status_code=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message="Tools retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="List all tools",
        description="Retrieve a list of all tools",
        tags=tags,
        responses=TOOLS_RESPONSE_EXAMPLE,
        auth=[],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
