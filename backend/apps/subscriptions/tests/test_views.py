from datetime import timedelta
from decimal import Decimal
from unittest.mock import MagicMock, patch

from apps.common.utils import TestUtil
from apps.subscriptions.choices import StatusChoices, SubscriptionChoices
from apps.subscriptions.models import PaymentTransaction, Subscription, SubscriptionPlan
from django.contrib.auth import get_user_model
from django.urls import reverse
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
