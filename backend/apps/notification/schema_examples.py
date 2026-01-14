from apps.common.schema_examples import ERR_RESPONSE_STATUS, SUCCESS_RESPONSE_STATUS
from apps.common.serializers import ErrorResponseSerializer, SuccessResponseSerializer
from apps.notification.serializers import NotificationSerializer
from drf_spectacular.utils import OpenApiExample, OpenApiResponse

NOTIFICATION_EXAMPLE = {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "actor_name": "John Doe",
    "recipient_name": "Jane Smith",
    "verb": "liked your post",
    "is_read": True,
    "created_at": "2024-01-14T17:34:53Z",
}

NOTIFICATION_RETRIEVE_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=NotificationSerializer,
        description="Notification retrieved and marked as read",
        examples=[
            OpenApiExample(
                name="Success Response",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Notification retrieved and marked as read.",
                    "data": NOTIFICATION_EXAMPLE,
                },
            ),
        ],
    ),
    404: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Notification not found",
        examples=[
            OpenApiExample(
                name="Not Found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Notification not found",
                    "code": "not_found",
                },
            ),
        ],
    ),
}

NOTIFICATION_DELETE_RESPONSE_EXAMPLE = {
    204: OpenApiResponse(
        description="Notification deleted successfully (No Content)",
    ),
    404: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Notification not found",
        examples=[
            OpenApiExample(
                name="Not Found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Notification not found",
                    "code": "not_found",
                },
            ),
        ],
    ),
}

NOTIFICATION_RESTORE_RESPONSE_EXAMPLE = {
    200: OpenApiResponse(
        response=NotificationSerializer,
        description="Notification restored successfully",
        examples=[
            OpenApiExample(
                name="Restored Successfully",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Notification restored successfully.",
                    "data": NOTIFICATION_EXAMPLE,
                },
            ),
            OpenApiExample(
                name="Already Active",
                value={
                    "status": SUCCESS_RESPONSE_STATUS,
                    "message": "Notification is not deleted.",
                },
            ),
        ],
    ),
    404: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Notification not found",
        examples=[
            OpenApiExample(
                name="Not Found",
                value={
                    "status": ERR_RESPONSE_STATUS,
                    "message": "Notification not found",
                    "code": "not_found",
                },
            ),
        ],
    ),
}
