from apps.common.exceptions import NotFoundError
from apps.common.responses import CustomResponse
from apps.content.filters import EventFilter, JobFilter
from apps.content.models import Category, Event, Job, Resource, Tool
from apps.content.schema_examples import (
    CATEGORY_DETAIL_RESPONSE_EXAMPLE,
    CATEGORY_RESPONSE_EXAMPLE,
    EVENT_DETAIL_RESPONSE_EXAMPLE,
    EVENTS_RESPONSE_EXAMPLE,
    JOB_DETAIL_RESPONSE_EXAMPLE,
    JOB_RESPONSE_EXAMPLE,
    RESOURCE_DETAIL_RESPONSE_EXAMPLE,
    RESOURCES_RESPONSE_EXAMPLE,
    TOOL_DETAIL_RESPONSE_EXAMPLE,
    TOOLS_RESPONSE_EXAMPLE,
)
from apps.content.serializers import (
    CategorySerializer,
    EventListSerializer,
    EventSerializer,
    JobListSerializer,
    JobSerializer,
    ResourceListSerializer,
    ResourceSerializer,
    ToolListSerializer,
    ToolSerializer,
)
from apps.general.views import CustomListView
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.views import APIView

tags = ["Contents"]


class CategoryGenericView(CustomListView):
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ["name"]
    ordering_fields = ["name"]
    queryset = Category.objects.all()

    @extend_schema(
        summary="List all categories",
        description="Retrieve a list of all blog categories. Categories are broad groupings used to organize articles and help users browse content by topic.",
        tags=tags,
        responses=CATEGORY_RESPONSE_EXAMPLE,
        auth=[],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class JobListView(CustomListView):
    serializer_class = JobListSerializer
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    filterset_class = JobFilter
    search_fields = ["title"]

    queryset = Job.active.select_related("category").all()

    @extend_schema(
        summary="List all jobs",
        description="Retrieve a list of all jobs",
        tags=tags,
        responses={200: JobListSerializer(many=True)},
        auth=[],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EventListView(CustomListView):
    serializer_class = EventListSerializer
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    filterset_class = EventFilter
    search_fields = ["title"]

    queryset = Event.objects.select_related("category").all()

    @extend_schema(
        summary="List all events.",
        description="Retrieve a list of all events. Accepted date format: YYYY-MM-DD e.g 2024-01-14",
        tags=tags,
        responses={200: EventListSerializer(many=True)},
        auth=[],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ResourceListView(CustomListView):
    serializer_class = ResourceListSerializer
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )

    filterset_fields = ("is_featured", "category")

    search_fields = ["name"]

    queryset = Resource.objects.select_related("category").all()

    @extend_schema(
        summary="List all resources",
        description="Retrieve a list of all resources",
        tags=tags,
        responses={200: ResourceListSerializer(many=True)},
        auth=[],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ToolListView(CustomListView):
    serializer_class = ToolListSerializer
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    filterset_fields = ("is_featured",)
    filterset_fields = ["category"]
    search_fields = ["name"]

    queryset = Tool.objects.select_related("category").prefetch_related("tags").all()

    @extend_schema(
        summary="List all tools",
        description="Retrieve a list of all tools",
        tags=tags,
        responses={200: ToolListSerializer(many=True)},
        auth=[],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CategoryRetrieveView(APIView):
    serializer_class = CategorySerializer

    @extend_schema(
        summary="Retrieve category details",
        description="Retrieve detailed information about a specific category by slug.",
        tags=tags,
        responses=CATEGORY_DETAIL_RESPONSE_EXAMPLE,
        auth=[],
    )
    def get(self, request, *args, **kwargs):
        try:
            category = Category.objects.get(slug=kwargs["slug"])
            serializer = self.serializer_class(category)
            return CustomResponse.success(
                message="Category detail retrieved successfully.",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
            )
        except Category.DoesNotExist:
            raise NotFoundError(err_msg="Category not found.")


class JobRetrieveView(APIView):
    serializer_class = JobSerializer

    @extend_schema(
        summary="Retrieve job details",
        description="Retrieve detailed information about a specific job posting by ID.",
        tags=tags,
        responses=JOB_DETAIL_RESPONSE_EXAMPLE,
        auth=[],
    )
    def get(self, request, *args, **kwargs):
        try:
            job = Job.active.select_related("category").get(id=kwargs["job_id"])
            serializer = self.serializer_class(job)
            return CustomResponse.success(
                message="Job detail retrieved successfully.",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
            )
        except Job.DoesNotExist:
            raise NotFoundError(err_msg="Job not found.")


class EventRetrieveView(APIView):
    serializer_class = EventSerializer

    @extend_schema(
        summary="Retrieve event details",
        description="Retrieve detailed information about a specific event by ID.",
        tags=tags,
        responses=EVENT_DETAIL_RESPONSE_EXAMPLE,
        auth=[],
    )
    def get(self, request, *args, **kwargs):
        try:
            event = Event.objects.select_related("category").get(id=kwargs["event_id"])
            serializer = self.serializer_class(event)
            return CustomResponse.success(
                message="Event detail retrieved successfully.",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
            )
        except Event.DoesNotExist:
            raise NotFoundError(err_msg="Event not found.")


class ResourceRetrieveView(APIView):
    serializer_class = ResourceSerializer

    @extend_schema(
        summary="Retrieve resource details",
        description="Retrieve detailed information about a specific resource by ID.",
        tags=tags,
        responses=RESOURCE_DETAIL_RESPONSE_EXAMPLE,
        auth=[],
    )
    def get(self, request, *args, **kwargs):
        try:
            resource = Resource.objects.select_related("category").get(
                id=kwargs["resource_id"]
            )
            serializer = self.serializer_class(resource)
            return CustomResponse.success(
                message="Resource detail retrieved successfully.",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
            )
        except Resource.DoesNotExist:
            raise NotFoundError(err_msg="Resource not found.")


class ToolRetrieveView(APIView):
    serializer_class = ToolSerializer

    @extend_schema(
        summary="Retrieve tool details",
        description="Retrieve detailed information about a specific tool by ID.",
        tags=tags,
        responses=TOOL_DETAIL_RESPONSE_EXAMPLE,
        auth=[],
    )
    def get(self, request, *args, **kwargs):
        try:
            tool = (
                Tool.objects.select_related("category")
                .prefetch_related("tags")
                .get(id=kwargs["tool_id"])
            )
            serializer = self.serializer_class(tool)
            return CustomResponse.success(
                message="Tool detail retrieved successfully.",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
            )
        except Tool.DoesNotExist:
            raise NotFoundError(err_msg="Tool not found.")
