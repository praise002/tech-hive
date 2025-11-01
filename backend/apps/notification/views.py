from apps.common.pagination import DefaultPagination
from apps.notification.models import Notification
from apps.notification.serializers import NotificationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

tags = ["Notifications"]


class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("is_read",)
    pagination_class = DefaultPagination

    def get_queryset(self):
        return Notification.objects.select_related("actor", "recipient").filter(
            recipient=self.request.user
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
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
