import logging

from apps.common.errors import ErrorCode
from apps.common.exceptions import NotFoundError
from apps.common.responses import CustomResponse
from apps.general.views import CustomListView
from apps.subscriptions.choices import SubscriptionChoices
from apps.subscriptions.schema_examples import (
    CANCEL_SUBSCRIPTION_RESPONSE_EXAMPLE,
    PAYMENT_HISTORY_RESPONSE_EXAMPLE,
    REACTIVATE_SUBSCRIPTION_RESPONSE_EXAMPLE,
    RETRY_PAYMENT_RESPONSE_EXAMPLE,
    SUBSCRIBE_TO_PREMIUM_RESPONSE_EXAMPLE,
    SUBSCRIPTION_DETAIL_RESPONSE_EXAMPLE,
    SUBSCRIPTION_PLAN_RESPONSE_EXAMPLE,
    UPDATE_PAYMENT_METHOD_RESPONSE_EXAMPLE,
)
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.views import APIView

from .models import PaymentTransaction, Subscription, SubscriptionPlan
from .serializers import (
    CancelRequestSerializer,
    PaymentCallbackResponseSerializer,
    PaymentTransactionSerializer,
    RetryPaymentResponseSerializer,
    SubscribeRequestSerializer,
    SubscriptionDetailSerializer,
    SubscriptionPlanSerializer,
    UpdateCardResponseSerializer,
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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message="Subscription plans retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="List all subscription plans",
        description="Retrieve a list of all active subscription plans available for purchase",
        tags=tags,
        responses=SUBSCRIPTION_PLAN_RESPONSE_EXAMPLE,
        auth=[],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SubscriptionPlanListAPIView(APIView):
    """
    Lists all active subscription plans available for purchase.
    """

    @extend_schema(
        summary="List all subscription plans",
        description="Retrieve a list of all active subscription plans available for purchase",
        tags=tags,
        # responses=SUBSCRIPTION_PLAN_RESPONSE_EXAMPLE,
        auth=[],
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

        subscription = Subscription.objects.get_latest_subscription(
            user=self.request.user
        )

        # NOTE: Frontend will display this:
        # "is_premium": False,
        # "current_plan": "Basic",
        # because using .first() returns NOne and doesn't raise error
        if not subscription:
            raise NotFoundError("Subscription not found")

        return subscription

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.success(
            message="Subscription retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Retrieve subscription",
        description="Retrieve the detailed status of the current user's subscription.",
        tags=tags,
        responses=SUBSCRIPTION_DETAIL_RESPONSE_EXAMPLE,
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class PaymentHistoryListView(CustomListView):
    """
    Provides a paginated list of the user's payment history.
    """

    queryset = PaymentTransaction.objects.all()
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
        # We are merging the PAYMENT_HISTORY_RESPONSE_EXAMPLE dictionary (which contains the 401)
        # with a dictionary that tells spectacular to generate the default for the 200 response.
        responses={
            200: PaymentTransactionSerializer(many=True),
            **PAYMENT_HISTORY_RESPONSE_EXAMPLE,
        },
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SubscribeToPremiumView(APIView):
    """
    Creates a new trial or paid subscription for a user.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubscribeRequestSerializer

    @extend_schema(
        summary="Create Subscription",
        description="Create a new trial or paid subscription for the authenticated user.",
        tags=tags,
        responses=SUBSCRIBE_TO_PREMIUM_RESPONSE_EXAMPLE,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        plan = validated_data["plan_id"]
        start_trial = validated_data["start_trial"]
        user = request.user

        try:
            if start_trial:
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
            return CustomResponse.error(
                message=str(e),
                err_code=ErrorCode.BAD_REQUEST,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except Exception as e:
            logger.error(f"Subscription creation failed for {user.email}: {e}")
            return CustomResponse.error(
                message="Failed to create subscription. Please try again.",
                err_code=ErrorCode.SERVER_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SubscriptionCancelAPIView(APIView):
    """
    Cancels a user's active subscription at the end of the billing period.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CancelRequestSerializer

    @extend_schema(
        summary="Cancel Subscription",
        description="Cancels the current user's active subscription. Access will remain until the end of the current billing period.",
        tags=tags,
        responses=CANCEL_SUBSCRIPTION_RESPONSE_EXAMPLE,
    )
    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        reason = serializer.validated_data.get("reason")
        user = request.user

        subscription = Subscription.objects.get_active_subscription(user)

        if not subscription:
            raise NotFoundError("No active subscription found")

        try:
            success = subscription_service.cancel_subscription(
                subscription=subscription, reason=reason
            )

            if not success:
                return CustomResponse.error(
                    message="Failed to cancel subscription",
                    err_code=ErrorCode.SERVER_ERROR,
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            response_data = {
                "access_until": subscription.current_period_end.strftime("%Y-%m-%d"),
            }

            return CustomResponse.success(
                message="Subscription cancelled successfully. Your access will continue until the end of the current period.",
                data=response_data,
                status_code=status.HTTP_200_OK,
            )

        except ValueError as e:
            return CustomResponse.error(
                message=str(e),
                err_code=ErrorCode.BAD_REQUEST,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except Exception as e:
            logger.error(f"Error cancelling subscription: {str(e)}")
            return CustomResponse.error(
                message="Failed to cancel subscription. Please try again.",
                err_code=ErrorCode.SERVER_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PaymentCallbackView(APIView):
    """
    Handle payment callback from Paystack.
    GET /api/subscriptions/payment/callback/?reference=TXN_xxxxx
    """

    serializer_class = PaymentCallbackResponseSerializer

    @extend_schema(exclude=True)
    def get(self, request, *args, **kwargs):
        reference = request.query_params.get("reference")

        if not reference:
            return CustomResponse.error(
                message="Payment reference is required",
                err_code=ErrorCode.BAD_REQUEST,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        try:
            success, message, _ = subscription_service.verify_and_activate_subscription(
                reference
            )

            if success:
                return CustomResponse.success(
                    message=message,
                    status_code=status.HTTP_200_OK,
                )
            else:
                return CustomResponse.error(
                    message=message,
                    err_code=ErrorCode.BAD_REQUEST,
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

        except Exception as e:
            logger.error(f"Error in payment callback: {str(e)}")
            return CustomResponse.error(
                message="Failed to process payment callback",
                err_code=ErrorCode.SERVER_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ReactivateSubscriptionView(APIView):
    """
    Reactivate a cancelled subscription.
    """

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Reactivate Subscription",
        description=(
            "Reactivates a subscription that was previously scheduled for cancellation. "
            "This removes the 'cancel_at_period_end' flag and ensures the subscription renews."
        ),
        tags=tags,
        request=None,  # No request body is needed for this action
        responses=REACTIVATE_SUBSCRIPTION_RESPONSE_EXAMPLE,
    )
    def post(self, request, *args, **kwargs):
        user = request.user

        subscription = (
            user.subscriptions.filter(status=SubscriptionChoices.CANCELLED)
            .order_by("-created_at")
            .first()
        )

        if not subscription:
            raise NotFoundError("No cancelled subscription found")

        try:
            success = subscription_service.reactivate_subscription(subscription)

            if not success:
                return CustomResponse.error(
                    message="Failed to reactivate subscription",
                    err_code=ErrorCode.SERVER_ERROR,
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return CustomResponse.success(
                message="Subscription reactivated successfully",
                data=SubscriptionDetailSerializer(subscription).data,
                status_code=status.HTTP_200_OK,
            )

        except ValueError as e:
            return CustomResponse.error(
                message=str(e),
                err_code=ErrorCode.BAD_REQUEST,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        except Exception as e:
            logger.error(f"Error reactivating subscription: {str(e)}")
            return CustomResponse.error(
                message="Failed to reactivate subscription",
                err_code=ErrorCode.SERVER_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RetryPaymentView(APIView):
    """
    Manually retry a failed payment.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RetryPaymentResponseSerializer

    @extend_schema(
        summary="Retry Failed Payment",
        description="For a subscription that is 'past_due', this endpoint attempts to charge the card on file again to make the subscription active.",
        tags=tags,
        request=None,
        responses=RETRY_PAYMENT_RESPONSE_EXAMPLE,
    )
    def post(self, request, *args, **kwargs):
        subscription = Subscription.objects.past_due().first()

        if not subscription:
            raise NotFoundError("No past due subscription found")

        try:

            success, message, transaction = subscription_service.retry_payment(
                subscription=subscription, is_manual=True
            )

            if not success:
                return CustomResponse.error(
                    message=message,
                    err_code=ErrorCode.BAD_REQUEST,
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

            return CustomResponse.success(
                message=message,
                data=PaymentTransactionSerializer(transaction).data,
                status_code=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"Error retrying payment: {str(e)}")
            return CustomResponse.error(
                message="Failed to retry payment",
                err_code=ErrorCode.SERVER_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UpdatePaymentMethodView(APIView):
    """
    Get link to update payment card.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdateCardResponseSerializer

    @extend_schema(
        summary="Get Payment Method Update Link",
        description="Generates and returns a unique URL from the payment provider that allows the user to securely update their card details.",
        tags=tags,
        request=None,
        responses=UPDATE_PAYMENT_METHOD_RESPONSE_EXAMPLE,
    )
    def get(self, request, *args, **kwargs):
        user = request.user

        subscription = Subscription.objects.get_active_subscription(user)

        if not subscription:
            raise NotFoundError("No active subscription found")

        try:
            update_link = subscription_service.update_payment_method(subscription)

            return CustomResponse.success(
                message="Visit this link to update your payment card",
                data={
                    "update_link": update_link,
                },
                status_code=status.HTTP_200_OK,
            )

        except ValueError as e:
            return CustomResponse.error(
                message=str(e),
                err_code=ErrorCode.BAD_REQUEST,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except Exception as e:
            logger.error(f"Error generating update link: {str(e)}")
            return CustomResponse.error(
                message="Failed to generate update link",
                err_code=ErrorCode.SERVER_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# Note: Other views like Reactivate, Retry Payment, Update Card, and Webhook
# would follow a similar pattern, using APIView for custom actions and
# calling the appropriate methods from `subscription_service` and `webhook_service`.
# calling the appropriate methods from `subscription_service` and `webhook_service`.
