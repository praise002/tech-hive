from apps.accounts.emails import SendEmail
from apps.common.exceptions import NotFoundError
from apps.common.pagination import DefaultPagination
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
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView

tags = ["General"]


class CustomListView(ListAPIView):
    pagination_class = DefaultPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data)
            return CustomResponse.success(
                message=f"{self.queryset.model._meta.verbose_name_plural} retrieved successfully.",
                data=paginated_data.data,
                status_code=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message=f"{self.queryset.model._meta.verbose_name_plural} retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class NewsletterView(APIView):
    serializer_class = NewsletterSerializer

    @extend_schema(
        summary="Subscribe to Newsletter",
        description="Subscribe to newsletter. You'll receive an email with an unsubscribe link.",
        tags=tags,
        responses=SUBSCRIBE_RESPONSE_EXAMPLE,
        auth=[],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscription = serializer.save()

        SendEmail.subscription(request, subscription)

        return CustomResponse.success(
            message="Subscribed to newsletter successfully.",
            status_code=status.HTTP_201_CREATED,
        )


class NewsletterUnsubscribeView(APIView):
    serializer_class = None
    
    @extend_schema(
        summary="Unsubscribe from Newsletter",
        description="Unsubscribe using the unique token from your newsletter email.",
        tags=tags,
        auth=[],
        responses=UNSUBSCRIBE_RESPONSE_EXAMPLE,
    )
    def get(self, request, token):
        """
        GET allows one-click unsubscribe from email clients
        """
        try:
            subscription = Newsletter.objects.get(
                unsubscribe_token=token, is_subscribed=True
            )
            subscription.is_subscribed = False
            subscription.unsubscribed_at = timezone.now()
            subscription.save()

            return CustomResponse.success(
                message="You have been unsubscribed from our newsletter.",
                status_code=status.HTTP_200_OK,
            )
        except Newsletter.DoesNotExist:
            raise NotFoundError("Invalid unsubscribe link or already unsubscribed.")


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
