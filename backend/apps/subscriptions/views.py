import logging

from amqp import NotFound
from apps.common.errors import ErrorCode
from apps.common.exceptions import NotFoundError
from apps.common.responses import CustomResponse
from apps.general.views import CustomListView
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.views import APIView

from .models import PaymentTransaction, Subscription, SubscriptionPlan
from .serializers import (
    CancelSubscriptionSerializer,
    CreateSubscriptionSerializer,
    PaymentTransactionSerializer,
    SubscriptionDetailSerializer,
    SubscriptionPlanSerializer,
)
from .services.subscription_service import subscription_service

logger = logging.getLogger(__name__)

tags = ["Subscriptions"]


class SubscriptionPlanListView(generics.ListAPIView):
    """
    Lists all active subscription plans available for purchase.
    """

    # queryset = SubscriptionPlan.objects.filter(is_active=True)
    queryset = SubscriptionPlan.objects.active()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message="Subscription plans retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="List all subscription plans",
        description="Retrieve a list of all active subscription plans available for purchase",
        tags=tags,
        # responses=SUBSCRIPTION_PLAN_RESPONSE_EXAMPLE,
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SubscriptionPlanListAPIView(APIView):
    """
    Lists all active subscription plans available for purchase.
    """

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="List all subscription plans",
        description="Retrieve a list of all active subscription plans available for purchase",
        tags=tags,
        # responses=SUBSCRIPTION_PLAN_RESPONSE_EXAMPLE,
    )
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to list active subscription plans.
        """
        plans = SubscriptionPlan.objects.filter(is_active=True)

        # The `many=True` argument is required when serializing a list of objects.
        serializer = SubscriptionPlanSerializer(plans, many=True)

        return CustomResponse.success(
            message="Subscription plans retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class SubscriptionDetailView(generics.RetrieveAPIView):
    """
    Retrieves the detailed status of the current user's subscription.
    """

    serializer_class = SubscriptionDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            subscription = Subscription.objects.get_latest_subscription(
                user=self.request.user
            )
            return subscription
        except Subscription.DoesNotExist:
            raise NotFoundError("Subscription not found")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.success(
            message="Subscription retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Retrieve subscription",
        description="Retrieve the detailed status of the current user's subscription.",
        tags=tags,
        # responses=SUBSCRIPTION_DETAIL_RESPONSE_EXAMPLE,
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class PaymentHistoryListView(CustomListView):
    """
    Provides a paginated list of the user's payment history.
    """

    serializer_class = PaymentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Returns all payment transactions for the currently authenticated user,
        ordered by the most recent first.
        """
        return PaymentTransaction.objects.filter(user=self.request.user).order_by(
            "-initiated_at"
        )

    @extend_schema(
        summary="List Payment History",
        description="Retrieve a paginated list of the current user's payment transactions.",
        tags=tags,
        # responses=PAYMENT_HISTORY_RESPONSE_EXAMPLE,
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SubscriptionCreateAPIView(APIView):
    """
    Creates a new trial or paid subscription for a user.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateSubscriptionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        plan = SubscriptionPlan.objects.get(id=validated_data["plan_id"])
        user = request.user

        try:
            if validated_data["start_trial"]:
                subscription, _ = subscription_service.start_trial(user=user, plan=plan)
                response_data = {
                    "status": subscription.status,
                    "trial_end": subscription.trial_end,
                }
                return CustomResponse.success(
                    message="7-day trial started successfully.",
                    data=response_data,
                    status_code=status.HTTP_201_CREATED,
                )

            else:
                # Create a paid subscription
                _, _, auth_url = subscription_service.create_paid_subscription(
                    user=user, plan=plan
                )
                response_data = {
                    "authorization_url": auth_url,
                }
                return CustomResponse.success(
                    message="Subscription initialized. Please proceed to payment.",
                    data=response_data,
                    status_code=status.HTTP_201_CREATED,
                )

        except ValueError as e:
            # Catches eligibility errors (e.g., not eligible for trial)
            CustomResponse.error(
                message=str(e),
                err_code=ErrorCode.BAD_REQUEST,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except Exception as e:
            logger.error(f"Subscription creation failed for {user.email}: {e}")
            return CustomResponse.error(
                message="An unexpected error occurred.",
                err_code=ErrorCode.BAD_REQUEST,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SubscriptionCancelAPIView(APIView):
    pass


#     """
#     Cancels a user's active subscription at the end of the billing period.
#     """

#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         serializer = CancelSubscriptionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         reason = serializer.validated_data.get("reason")

#         subscription = Subscription.objects.get_active_subscription(user=request.user)
#         if not subscription:
#             return Response(
#                 {"error": "No active subscription found to cancel."},
#                 status=status.HTTP_404_NOT_FOUND,
#             )

#         try:
#             subscription_service.cancel_subscription(subscription, reason)
#             return Response(
#                 {
#                     "message": "Subscription cancelled successfully. Your access will continue until the end of the current period.",
#                     "access_until": subscription.current_period_end,
#                 },
#                 status=status.HTTP_200_OK,
#             )
#         except ValueError as e:
#             # Catches errors like "already cancelled"
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             logger.error(
#                 f"Subscription cancellation failed for {request.user.email}: {e}"
#             )
#             return Response(
#                 {"error": "An unexpected error occurred during cancellation."},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )


# # Note: Other views like Reactivate, Retry Payment, Update Card, and Webhook
# # would follow a similar pattern, using APIView for custom actions and
# # calling the appropriate methods from `subscription_service` and `webhook_service`.
