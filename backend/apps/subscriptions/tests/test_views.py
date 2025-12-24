from datetime import timedelta
from decimal import Decimal
from unittest.mock import MagicMock, patch

from apps.common.utils import TestUtil
from apps.subscriptions.choices import StatusChoices, SubscriptionChoices
from apps.subscriptions.models import PaymentTransaction, Subscription, SubscriptionPlan
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class SubscriptionAPITestCase(APITestCase):
    """Base test case for subscription API tests"""

    def setUp(self):
        """Set up test data and authentication"""
        self.user1 = TestUtil.verified_user()

        self.user2 = TestUtil.other_verified_user()

        self.plan = SubscriptionPlan.objects.create(
            name="Premium Monthly",
            price=Decimal("5000.00"),
            billing_cycle="MONTHLY",
            paystack_plan_code="PLN_test123",
            features={"max_articles": 100},
        )


class SubscribeToPremiumViewTest(SubscriptionAPITestCase):
    """Test subscribe to premium endpoint"""

    url = "/api/v1/subscriptions/premium/"

    @patch("apps.subscriptions.views.subscription_service")
    def test_start_trial_success(self, mock_service):
        """Test starting trial successfully"""
        # Mock service response
        subscription = Subscription(
            user=self.user1,
            plan=self.plan,
            status=SubscriptionChoices.TRIALING,
            trial_start=timezone.now(),
            trial_end=timezone.now() + timedelta(days=7),
        )

        transaction = PaymentTransaction(
            user=self.user1,
            subscription=subscription,
            reference="TXN_test123",
            amount=self.plan.price,
            status=StatusChoices.SUCCESS,
        )

        mock_service.start_trial.return_value = (subscription, transaction)

        self.client.force_authenticate(self.user1)
        response = self.client.post(
            self.url,
            {"plan_id": str(self.plan.id), "start_trial": True},
        )
        print(response.data)

        response_data = response.data["data"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("trial_end", response_data)
        self.assertEqual(response_data["status"], SubscriptionChoices.TRIALING)
        self.assertEqual(response_data.get("payment_url"), None)
        self.assertIn("trial started successfully", response.data["message"])

    @patch("apps.subscriptions.views.subscription_service")
    def test_create_paid_subscription_success(self, mock_service):
        """Test creating paid subscription successfully"""
        # Mock service response
        subscription = Subscription(
            user=self.user1,
            plan=self.plan,
            status=SubscriptionChoices.TRIALING,
            reference="TXN_test123",
        )

        transaction = PaymentTransaction(
            user=self.user1,
            subscription=subscription,
            reference="TXN_test123",
            amount=self.plan.price,
            status=StatusChoices.PENDING,
        )

        payment_url = "https://checkout.paystack.com/test123"

        mock_service.create_paid_subscription.return_value = (
            subscription,
            transaction,
            payment_url,
        )

        self.client.force_authenticate(self.user1)
        response = self.client.post(
            self.url,
            {"plan_id": str(self.plan.id), "start_trial": False},
        )

        response_data = response.data
        print(response_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["data"]["authorization_url"], payment_url)

    def test_subscribe_missing_plan_id(self):
        """Test subscribing without plan_id fails"""
        self.client.force_authenticate(self.user1)
        response = self.client.post(self.url, {"start_trial": False})

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        print(response.data)

    def test_subscribe_invalid_plan_id(self):
        """Test subscribing with invalid plan_id fails"""
        self.client.force_authenticate(self.user1)
        response = self.client.post(
            self.url,
            {"plan_id": "00000000-0000-0000-0000-000000000000", "start_trial": False},
        )

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        print(response.data)

    def test_subscribe_user_already_has_subscription(self):
        """Test subscribing when user already has subscription"""
        # Create existing subscription
        Subscription.objects.create(
            user=self.user1,
            plan=self.plan,
            status=SubscriptionChoices.ACTIVE,
            reference="TXN_existing",
        )

        self.client.force_authenticate(self.user1)
        response = self.client.post(
            self.url, {"plan_id": str(self.plan.id), "start_trial": False}
        )

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        print(response.data)
        self.assertIn(
            "already has an active subscription", str(response.data["message"])
        )

    def test_subscribe_unauthenticated(self):
        """Test subscribing without authentication fails"""
        response = self.client.post(
            self.url, {"plan_id": str(self.plan.id), "start_trial": False}
        )
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PaymentCallbackViewTest(SubscriptionAPITestCase):
    """Test payment callback endpoint"""

    url = "/api/v1/subscriptions/payment/callback/"

    @patch("apps.subscriptions.views.subscription_service")
    def test_payment_callback_success(self, mock_service):
        """Test successful payment callback"""
        subscription = Subscription.objects.create(
            user=self.user1,
            plan=self.plan,
            status=SubscriptionChoices.ACTIVE,
            reference="TXN_test123",
        )

        transaction = PaymentTransaction.objects.create(
            user=self.user1,
            subscription=subscription,
            reference="TXN_test123",
            amount=self.plan.price,
            status=StatusChoices.SUCCESS,
        )

        # Mock service response
        mock_service.verify_and_activate_subscription.return_value = (
            True,
            "Payment successful",
            transaction,
        )

        self.client.force_authenticate(self.user1)
        response = self.client.get(self.url, {"reference": "TXN_test123"})
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Payment successful", response.data["message"])

    @patch("apps.subscriptions.views.subscription_service")
    def test_payment_callback_failed(self, mock_service):
        """Test failed payment callback"""
        # Mock service response
        mock_service.verify_and_activate_subscription.return_value = (
            False,
            "Payment failed",
            None,
        )

        self.client.force_authenticate(self.user1)
        response = self.client.get(self.url, {"reference": "TXN_test123"})
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

        self.assertIn("Payment failed", response.data["message"])

    def test_payment_callback_missing_reference(self):
        """Test callback without reference fails"""
        self.client.force_authenticate(self.user1)
        response = self.client.get(self.url)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn("reference", str(response.data).lower())


class SubscriptionDetailsViewTest(SubscriptionAPITestCase):
    """Test subscription details endpoint"""

    url = "/api/v1/subscriptions/me/"

    def test_get_subscription_details_with_subscription(self):
        """Test getting details when user has subscription"""
        _ = Subscription.objects.create(
            user=self.user1,
            plan=self.plan,
            status=SubscriptionChoices.ACTIVE,
            start_date=timezone.now(),
            current_period_start=timezone.now(),
            current_period_end=timezone.now() + timedelta(days=30),
            next_billing_date=timezone.now() + timedelta(days=30),
            card_last4="1234",
            card_type="visa",
            card_bank="Access Bank",
            reference="TXN_active123",
        )

        self.client.force_authenticate(self.user1)
        response = self.client.get(self.url)
        print(response.data)
        response_data = response.data["data"]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response_data["is_premium"])
        self.assertEqual(response_data["status"], "ACTIVE")

    def test_get_subscription_details_without_subscription(self):
        """Test getting details when user has no subscription"""

        self.client.force_authenticate(self.user1)
        response = self.client.get(self.url)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_subscription_details_unauthenticated(self):
        """Test getting details without authentication fails"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CancelSubscriptionViewTest(SubscriptionAPITestCase):
    """Test cancel subscription endpoint"""

    url = "/api/v1/subscriptions/premium/cancel/"

    @patch("apps.subscriptions.services.subscription_service.notification_service")
    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_cancel_subscription_success(self, mock_paystack, mock_notification):
        """Test cancelling subscription successfully"""

        subscription = Subscription.objects.create(
            user=self.user1,
            plan=self.plan,
            status=SubscriptionChoices.ACTIVE,
            reference="TXN_test123",
            current_period_end=timezone.now() + timedelta(days=20),
            paystack_subscription_code="SUB_test123",
            paystack_email_token="test-token",
        )

        mock_paystack.disable_subscription.return_value = True

        self.client.force_authenticate(self.user1)
        response = self.client.patch(self.url, {"reason": "Too expensive"})
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("cancelled successfully", response.data["message"])
        mock_notification.send_cancellation_confirmed_email.assert_called_once()

        # Verify real changes happened
        subscription.refresh_from_db()
        self.assertEqual(subscription.status, SubscriptionChoices.CANCELLED)
        self.assertEqual(subscription.cancel_reason, "Too expensive")

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_cancel_subscription_no_active_subscription(self, mock_paystack):
        """Test cancelling when user has no subscription"""

        self.client.force_authenticate(self.user1)
        response = self.client.patch(
            self.url,
            {"reason": "Testing"},
        )
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("No active subscription", str(response.data))

        # Verify Paystack was NOT called
        mock_paystack.disable_subscription.assert_not_called()

    def test_cancel_subscription_unauthenticated(self):
        """Test cancelling without authentication fails"""
        response = self.client.post(self.url, {"reason": "Test"})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReactivateSubscriptionViewTest(SubscriptionAPITestCase):
    """Test reactivate subscription endpoint"""

    url = "/api/v1/subscriptions/reactivate/"

    @patch("apps.subscriptions.services.subscription_service")
    def test_reactivate_subscription_success(self, mock_service):
        """Test reactivating subscription successfully"""
        Subscription.objects.create(
            user=self.user2,
            plan=self.plan,
            status=SubscriptionChoices.CANCELLED,
            reference="TXN_test123",
            cancelled_at=timezone.now() - timedelta(days=1),
            current_period_end=timezone.now() + timedelta(days=20),
        )

        # Mock service response
        mock_service.reactivate_subscription.return_value = True

        self.client.force_authenticate(self.user2)
        response = self.client.post(self.url)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("reactivated successfully", response.data["message"])

    def test_reactivate_subscription_no_cancelled_subscription(self):
        """Test reactivating when no cancelled subscription"""
        self.client.force_authenticate(self.user2)
        response = self.client.post(self.url)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("No cancelled subscription", str(response.data))

    def test_reactivate_subscription_unauthenticated(self):
        """Test reactivating without authentication fails"""
        response = self.client.post(self.url)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RetryPaymentViewTest(SubscriptionAPITestCase):
    """Test retry payment endpoint"""

    url = "/api/v1/subscriptions/payment-retry/"

    @patch("apps.subscriptions.views.subscription_service")
    def test_retry_payment_success(self, mock_service):
        """Test retrying payment successfully"""
        # Create PAST_DUE subscription
        subscription = Subscription.objects.create(
            user=self.user1,
            plan=self.plan,
            status=SubscriptionChoices.PAST_DUE,
            reference="TXN_test123",
            payment_failed_at=timezone.now() - timedelta(days=3),
            retry_count=1,
        )

        # Create transaction
        transaction = PaymentTransaction.objects.create(
            user=self.user1,
            subscription=subscription,
            reference="TXN_retry",
            amount=self.plan.price,
            status=StatusChoices.SUCCESS,
        )

        # Mock service response
        mock_service.retry_payment.return_value = (
            True,
            "Payment successful",
            transaction,
        )

        self.client.force_authenticate(self.user1)
        response = self.client.post(self.url)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Payment successful", response.data["message"])

    @patch("apps.subscriptions.views.subscription_service")
    def test_retry_payment_failure(self, mock_service):
        """Test retrying payment failure"""
        # Create PAST_DUE subscription
        Subscription.objects.create(
            user=self.user1,
            plan=self.plan,
            status=SubscriptionChoices.PAST_DUE,
            reference="TXN_test123",
            payment_failed_at=timezone.now() - timedelta(days=3),
            retry_count=1,
        )

        # Mock service response
        mock_service.retry_payment.return_value = (False, "Insufficient funds", None)

        self.client.force_authenticate(self.user1)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn("Insufficient funds", response.data["message"])

    def test_retry_payment_no_past_due_subscription(self):
        """Test retrying when no PAST_DUE subscription"""
        self.client.force_authenticate(self.user1)
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("No past due subscription", str(response.data))

    def test_retry_payment_unauthenticated(self):
        """Test retrying without authentication fails"""
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdatePaymentMethodViewTest(SubscriptionAPITestCase):
    """Test update payment method endpoint"""

    url = "/api/v1/subscriptions/card-update/"

    @patch("apps.subscriptions.views.subscription_service")
    def test_update_payment_method_success(self, mock_service):
        """Test getting update link successfully"""

        Subscription.objects.create(
            user=self.user2,
            plan=self.plan,
            status=SubscriptionChoices.ACTIVE,
            reference="TXN_test123",
            paystack_subscription_code="SUB_test123",
        )

        # Mock service response
        update_link = "https://api.paystack.co/subscription/manage/link/abc123"
        mock_service.update_payment_method.return_value = update_link

        self.client.force_authenticate(self.user2)
        response = self.client.get(self.url)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["update_link"], update_link)

    def test_update_payment_method_no_subscription(self):
        """Test getting update link without subscription"""
        self.client.force_authenticate(self.user2)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("No active subscription", str(response.data))

    def test_update_payment_method_unauthenticated(self):
        """Test getting update link without authentication fails"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PaymentHistoryViewTest(SubscriptionAPITestCase):
    """Test payment history endpoint"""

    url = "/api/v1/subscriptions/payment-history/"

    def test_get_payment_history_success(self):
        """Test getting payment history successfully"""

        subscription = Subscription.objects.create(
            user=self.user1,
            plan=self.plan,
            status=SubscriptionChoices.ACTIVE,
            reference="TXN_test123",
        )

        PaymentTransaction.objects.create(
            user=self.user1,
            subscription=subscription,
            reference="TXN_001",
            amount=self.plan.price,
            status=StatusChoices.SUCCESS,
        )

        PaymentTransaction.objects.create(
            user=self.user1,
            subscription=subscription,
            reference="TXN_002",
            amount=self.plan.price,
            status=StatusChoices.SUCCESS,
        )

        self.client.force_authenticate(self.user1)
        response = self.client.get(self.url)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]["results"]), 2)

    def test_get_payment_history_user_isolation(self):
        """Test users only see their own transactions"""
        # Create subscriptions for both users
        sub1 = Subscription.objects.create(
            user=self.user1,
            plan=self.plan,
            status=SubscriptionChoices.ACTIVE,
            reference="TXN_user1",
        )

        sub2 = Subscription.objects.create(
            user=self.user2,
            plan=self.plan,
            status=SubscriptionChoices.ACTIVE,
            reference="TXN_user2",
        )

        # Create transactions for both users
        PaymentTransaction.objects.create(
            user=self.user1,
            subscription=sub1,
            reference="TXN_user1_001",
            amount=self.plan.price,
            status=StatusChoices.SUCCESS,
        )

        PaymentTransaction.objects.create(
            user=self.user2,
            subscription=sub2,
            reference="TXN_user2_001",
            amount=self.plan.price,
            status=StatusChoices.SUCCESS,
        )

        # User1 makes request
        self.client.force_authenticate(self.user1)
        response = self.client.get(self.url)
        print(response.data)

        # Assert user1 only sees their transaction
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]["results"]), 1)
        self.assertEqual(
            response.data["data"]["results"][0]["reference"], "TXN_user1_001"
        )

    def test_get_payment_history_empty(self):
        """Test getting empty payment history"""
        self.client.force_authenticate(self.user1)
        response = self.client.get(self.url)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]["results"]), 0)

    def test_get_payment_history_unauthenticated(self):
        """Test getting history without authentication fails"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SubscriptionPlanListViewTest(SubscriptionAPITestCase):
    """Test subscription plan list endpoint"""

    url = "/api/v1/subscriptions/plans/"

    def test_list_plans_success(self):
        """Test listing active plans"""
        # Create inactive plan
        SubscriptionPlan.objects.create(
            name="Inactive Plan",
            price=Decimal("3000.00"),
            billing_cycle="MONTHLY",
            paystack_plan_code="PLN_inactive",
            is_active=False,
        )

        response = self.client.get(self.url)
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only return the active plan from setUp
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["name"], "Premium Monthly")

    def test_list_plans_no_authentication_required(self):
        """Test listing plans doesn't require authentication"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PaystackWebhookViewTest(SubscriptionAPITestCase):
    """Test Paystack webhook endpoint"""

    url = "/api/v1/subscriptions/webhook/"

    @patch("apps.subscriptions.services.webhook_service.WebhookService.process_webhook")
    def test_webhook_success(self, mock_service):
        """Test successful webhook processing"""
        # Mock service response
        mock_service.process_webhook.return_value = True

        # Prepare webhook data
        payload = {
            "event": "charge.success",
            "data": {"reference": "TXN_test123", "status": "success"},
        }

        response = self.client.post(
            self.url, payload, format="json", HTTP_X_PAYSTACK_SIGNATURE="test_signature"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # TODO: STILLL FAILING
    # @patch("apps.subscriptions.services.webhook_service.WebhookService.process_webhook")
    # def test_webhook_invalid_signature(self, mock_service):
    #     """Test webhook with invalid signature"""
    #     # Mock service response
    #     mock_service.process_webhook.return_value = False

    #     # Prepare webhook data
    #     payload = {"event": "charge.success", "data": {}}

    #     # Make request
    #     response = self.client.post(
    #         self.url,
    #         payload,
    #         format="json",
    #         HTTP_X_PAYSTACK_SIGNATURE="invalid_signature",
    #     )

    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_webhook_missing_signature(self):
    #     """Test webhook without signature header"""
    #     payload = {"event": "charge.success", "data": {}}

    #     # Make request without signature
    #     response = self.client.post(self.url, payload, format="json")

    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_webhook_missing_event_type(self):
    #     """Test webhook without event type"""
    #     payload = {"data": {}}

    #     response = self.client.post(
    #         self.url, payload, format="json", HTTP_X_PAYSTACK_SIGNATURE="test_signature"
    #     )

    #     # Assert response
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
