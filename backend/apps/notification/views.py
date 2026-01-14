from apps.common.exceptions import NotFoundError
from apps.common.pagination import DefaultPagination
from apps.common.responses import CustomResponse
from apps.notification.models import Notification
from apps.notification.schema_examples import (
    NOTIFICATION_DELETE_RESPONSE_EXAMPLE,
    NOTIFICATION_RESTORE_RESPONSE_EXAMPLE,
    NOTIFICATION_RETRIEVE_RESPONSE_EXAMPLE,
)
from apps.notification.serializers import NotificationSerializer
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

tags = ["Notifications"]


class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("is_read",)
    pagination_class = DefaultPagination
    queryset = Notification.objects.none()

    def get_queryset(self):
        return Notification.objects.select_related(
            "actor", "recipient", "target_ct"
        ).filter(recipient=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            # We don't mark as read here as it's a list view
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data)
            return CustomResponse.success(
                message="Notifications retrieved successfully.",
                data=paginated_data.data,
                status_code=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message="Notifications retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Retrieve user notifications",
        description="This endpoint retrieves a paginated list of notifications for the authenticated user. It allows filtering by read status (`is_read=true` or `is_read=false`).",
        tags=tags,
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class NotificationDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    @extend_schema(
        summary="Retrieve a single notification",
        description="Retrieves a single notification by ID and automatically marks it as read.",
        responses=NOTIFICATION_RETRIEVE_RESPONSE_EXAMPLE,
        tags=tags,
    )
    def get(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, recipient=request.user)
        except Notification.DoesNotExist:
            raise NotFoundError("Notification not found")

        # Auto-mark as read
        if not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=["is_read"])

        serializer = self.serializer_class(notification)
        return CustomResponse.success(
            message="Notification retrieved and marked as read.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Soft-delete a notification",
        description="Marks a notification as deleted. This can be undone using the restore endpoint.",
        responses=NOTIFICATION_DELETE_RESPONSE_EXAMPLE,
        tags=tags,
    )
    def delete(self, request, pk):
        try:
            notification = Notification.objects.get(pk=pk, recipient=request.user)
        except Notification.DoesNotExist:
            raise NotFoundError("Notification not found")

        notification.delete()  # Inherited IsDeletedModel.delete() does a soft-delete
        return Response(status=status.HTTP_204_NO_CONTENT)


class NotificationRestoreView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    @extend_schema(
        summary="Restore a deleted notification",
        description="Restores a previously soft-deleted notification.",
        responses=NOTIFICATION_RESTORE_RESPONSE_EXAMPLE,
        tags=tags,
    )
    def post(self, request, pk):
        # We use unfiltered() because the default manager excludes is_deleted=True
        try:
            notification = Notification.objects.unfiltered().get(
                pk=pk, recipient=request.user
            )
        except Notification.DoesNotExist:
            raise NotFoundError("Notification not found")

        if notification.is_deleted:
            notification.is_deleted = False
            notification.deleted_at = None
            notification.save(update_fields=["is_deleted", "deleted_at"])

            serializer = self.serializer_class(notification)
            return CustomResponse.success(
                message="Notification restored successfully.",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
            )

        return CustomResponse.success(
            message="Notification is not deleted.",
            status_code=status.HTTP_200_OK,
        )
