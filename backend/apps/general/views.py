from apps.common.errors import ErrorCode
from apps.common.responses import CustomResponse
from apps.general.models import Newsletter, SiteDetail
from apps.general.schema_examples import (
    CONTACT_RESPONSE_EXAMPLE,
    SITE_DETAIL_RESPONSE_EXAMPLE,
    SUBSCRIBE_RESPONSE_EXAMPLE,
    UNSUBSCRIBE_RESPONSE_EXAMPLE,
)
from apps.general.serializer import (
    ContactSerializer,
    NewsletterSerializer,
    SiteDetailSerializer,
)
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

tags = ["General"]


class NewsletterView(APIView):
    serializer_class = NewsletterSerializer

    @extend_schema(
        summary="Subscribe to Newsletter",
        description="This endpoint allows users to subscribe to newsletter",
        tags=tags,
        responses=SUBSCRIBE_RESPONSE_EXAMPLE,
        auth=[],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return CustomResponse.success(
            message="Subscribed to newsletter successfully.",
            status_code=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary="Unsubscribe to Newsletter",
        description="This endpoint allows users to unsubscribe to newsletter",
        tags=tags,
        parameters=[
            OpenApiParameter(
                name="email",
                type=str,
                location=OpenApiParameter.QUERY,
                required=True,
                description="Email address to unsubscribe",
                # examples=[
                #     OpenApiExample(
                #         "Example Request",
                #         value="user@example.com",
                #     )
                # ],
            )
        ],
        responses=UNSUBSCRIBE_RESPONSE_EXAMPLE,
        auth=[],
    )
    def delete(self, request):
        email = request.query_params.get("email")
        if not email:
            return CustomResponse.error(
                message="Email parameter is required.",
                err_code=ErrorCode.VALIDATION_ERROR,
            )

        try:
            subscription = Newsletter.objects.get(email=email)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Newsletter.DoesNotExist:
            return CustomResponse.error(
                message="Subscription not found for the provided email.",
                err_code=ErrorCode.VALIDATION_ERROR,
            )


class NewsletterGenericView(CreateAPIView):
    serializer_class = NewsletterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return CustomResponse.success(
            message="Subscribed to newsletter successfully.",
            status_code=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary="Subscribe to Newsletter",
        description="This endpoint allows users to subscribe to newsletter",
        tags=tags,
        responses=SUBSCRIBE_RESPONSE_EXAMPLE,
        auth=[],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SiteDetailView(APIView):
    serializer_class = SiteDetailSerializer

    @extend_schema(
        summary="Retrieve the single SiteDetail object",
        description="This endpoint retrieves the single SiteDetail object",
        tags=tags,
        responses=SITE_DETAIL_RESPONSE_EXAMPLE,
        auth=[],
    )
    def get(self, request):
        site_detail, _ = SiteDetail.objects.get_or_create()
        serializer = self.serializer_class(site_detail)
        return CustomResponse.success(
            message="Site detail retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class SiteDetailGenericView(RetrieveAPIView):
    serializer_class = SiteDetailSerializer

    def get_object(self):
        obj, _ = SiteDetail.objects.get_or_create()
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.success(
            message="Site detail retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Retrieve the single SiteDetail object",
        description="This endpoint retrieves the single SiteDetail object",
        tags=tags,
        responses=SITE_DETAIL_RESPONSE_EXAMPLE,
        auth=[],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ContactView(APIView):
    serializer_class = ContactSerializer

    @extend_schema(
        summary="Create a new Contact object",
        description="This endpoint creates a new Contact object",
        tags=tags,
        responses=CONTACT_RESPONSE_EXAMPLE,
        auth=[],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return CustomResponse.success(
            message="Message sent successfully.",
            status_code=status.HTTP_201_CREATED,
        )


class ContactGenericView(CreateAPIView):
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return CustomResponse.success(
            message="Message sent successfully.",
            status_code=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary="Create a new Contact object",
        description="This endpoint creates a new Contact object",
        tags=tags,
        responses=CONTACT_RESPONSE_EXAMPLE,
        auth=[],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
