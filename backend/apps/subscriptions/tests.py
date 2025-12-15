from decimal import Decimal
from unittest.mock import patch

from apps.common.utils import TestUtil
from apps.subscriptions.choices import (
    StatusChoices,
    SubscriptionChoices,
    TransactionTypeChoices,
)
from apps.subscriptions.models import PaymentTransaction, Subscription, SubscriptionPlan
from apps.subscriptions.services.subscription_service import subscription_service
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase

User = get_user_model()


class StartTrialTestCase(APITestCase):
    """Test cases for subscription_service.start_trial()"""

    def setUp(self):
        """Set up test data"""
        self.plan = SubscriptionPlan.objects.create(
            name="Premium Monthly",
            price=Decimal("5000.00"),
            billing_cycle="MONTHLY",
            paystack_plan_code="PLN_test123",
            features={"max_articles": 100},
        )
        self.user = TestUtil.verified_user()

    def test_start_trial_success(self):
        """Test successful trial creation for a new user"""

        subscription, transaction = subscription_service.start_trial(
            user=self.user, plan=self.plan
        )

        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.plan, self.plan)
        self.assertEqual(subscription.status, SubscriptionChoices.TRIALING)
        self.assertIsNotNone(subscription.trial_start)
        self.assertIsNotNone(subscription.trial_end)
        self.assertEqual(subscription.next_billing_date, subscription.trial_end)
        self.assertIsNone(
            subscription.current_period_start
        )  # No billing periods during trial
        self.assertIsNone(subscription.current_period_end)

        # Check trial duration (7 days)
        trial_duration = subscription.trial_end - subscription.trial_start
        self.assertEqual(trial_duration.days, 7)

        # Assertions for PaymentTransaction
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.subscription, subscription)
        self.assertEqual(transaction.amount, self.plan.price)  # Full price stored
        self.assertEqual(transaction.status, StatusChoices.SUCCESS)
        self.assertEqual(
            transaction.transaction_type, TransactionTypeChoices.SUBSCRIPTION
        )
        self.assertIsNotNone(transaction.reference)
        self.assertTrue(transaction.reference.startswith("TXN_"))

    def test_start_trial_user_already_has_active_subscription(self):
        """Test failure when user already has an active subscription"""
        # Create an existing active subscription
        Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            status=SubscriptionChoices.ACTIVE,
            start_date=timezone.now(),
        )

        with self.assertRaises(ValueError) as context:
            subscription_service.start_trial(user=self.user, plan=self.plan)

        self.assertIn("User already has an active subscription", str(context.exception))

    def test_start_trial_user_not_eligible_previous_subscription(self):
        """Test failure when user has a previous subscription (not eligible for trial)"""
        # Create a previous expired subscription
        Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            status=SubscriptionChoices.EXPIRED,
            start_date=timezone.now() - timezone.timedelta(days=30),
            expires_at=timezone.now() - timezone.timedelta(days=1),
        )

        with self.assertRaises(ValueError) as context:
            subscription_service.start_trial(user=self.user, plan=self.plan)

        self.assertIn("User is not eligible for trial", str(context.exception))

    def test_start_trial_invalid_plan(self):
        """Test failure with invalid plan (should fail at model level)"""
        invalid_plan = SubscriptionPlan.objects.create(
            name="Invalid Plan",
            price=Decimal("0.00"),  # Invalid price (below min validator)
            billing_cycle="MONTHLY",
            paystack_plan_code="PLN_invalid",
            features={},
        )
        print(invalid_plan)

        # This should raise ValidationError from the model validator
        with self.assertRaises(Exception):  # Could be ValidationError or ValueError
            subscription_service.start_trial(user=self.user, plan=invalid_plan)


class CreatePaidSubscriptionTestCase(APITestCase):
    """Test cases for subscription_service.create_paid_subscription()"""

    def setUp(self):
        """Set up test data"""
        self.plan = SubscriptionPlan.objects.create(
            name="Premium Monthly",
            price=Decimal("5000.00"),
            billing_cycle="MONTHLY",
            paystack_plan_code="PLN_test123",
            features={"max_articles": 100},
        )
        self.user = TestUtil.verified_user()

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_create_paid_subscription_success(self, mock_paystack):
        """Test successful paid subscription creation with Paystack initialization"""

        mock_paystack.initialize_transaction.return_value = {
            "authorization_url": "https://checkout.paystack.com/test123",
            "access_code": "test_access_code",
            "reference": "test_reference_from_paystack",
        }

        subscription, transaction, auth_url = (
            subscription_service.create_paid_subscription(
                user=self.user, plan=self.plan
            )
        )

        # Assertions for Subscription
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.plan, self.plan)
        self.assertIsNone(subscription.status)  # Initial status before payment
        self.assertIsNotNone(subscription.start_date)
        print(f"Start date {subscription.start_date}")
        self.assertIsNotNone(subscription.reference)
        self.assertTrue(subscription.reference.startswith("TXN_"))
        print(f"Reference {subscription.reference}")

        # No trial for paid subscriptions
        self.assertIsNone(subscription.trial_start)
        self.assertIsNone(subscription.trial_end)

        # Billing periods are set by webhook after payment
        self.assertIsNone(subscription.current_period_start)
        self.assertIsNone(subscription.current_period_end)
        print(f"Current billing period end {subscription.current_period_end}")
        self.assertIsNone(subscription.next_billing_date)

        # Assertions for PaymentTransaction
        self.assertEqual(transaction.user, self.user)
        self.assertEqual(transaction.subscription, subscription)
        self.assertEqual(transaction.amount, self.plan.price)
        self.assertEqual(
            transaction.status, StatusChoices.PENDING
        )  # Pending until payment verified
        self.assertEqual(
            transaction.transaction_type, TransactionTypeChoices.SUBSCRIPTION
        )
        self.assertIsNotNone(transaction.reference)
        self.assertEqual(transaction.reference, subscription.reference)

        # Assertions for Paystack integration
        self.assertEqual(auth_url, "https://checkout.paystack.com/test123")

        # Verify Paystack was called with correct parameters
        mock_paystack.initialize_transaction.assert_called_once()
        call_args = mock_paystack.initialize_transaction.call_args[1]

        self.assertEqual(call_args["email"], self.user.email)
        self.assertEqual(call_args["amount"], self.plan.price)
        self.assertEqual(call_args["plan_code"], self.plan.paystack_plan_code)
        self.assertIn("callback_url", call_args)
        self.assertIn("metadata", call_args)
        self.assertEqual(call_args["reference"], subscription.reference)
        print(call_args["reference"])

        # Verify metadata contains required fields
        metadata = call_args["metadata"]
        self.assertEqual(metadata["user_id"], str(self.user.id))
        self.assertEqual(metadata["user_email"], self.user.email)
        self.assertEqual(metadata["plan_id"], str(self.plan.id))
        self.assertEqual(metadata["plan_name"], self.plan.name)
        self.assertEqual(metadata["subscription_id"], str(subscription.id))

    def test_create_paid_subscription_user_already_has_active_subscription(self):
        """Test failure when user already has an active subscription"""

        # Create an existing active subscription
        Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            status=SubscriptionChoices.ACTIVE,
            start_date=timezone.now(),
            reference="TXN_EXISTING123",
        )

        with self.assertRaises(ValueError) as context:
            subscription_service.create_paid_subscription(
                user=self.user, plan=self.plan
            )
        print(str(context.exception))
        self.assertIn("User already has an active subscription", str(context.exception))

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_create_paid_subscription_paystack_api_fails(self, mock_paystack):
        """Test failure when Paystack API call fails"""

        # Mock Paystack to raise an exception
        mock_paystack.initialize_transaction.side_effect = Exception(
            "Paystack API error: Network timeout"
        )

        with self.assertRaises(Exception) as context:
            subscription_service.create_paid_subscription(
                user=self.user, plan=self.plan
            )

        self.assertIn("Failed to create subscription", str(context.exception))

        # Verify no subscription or transaction was created
        self.assertEqual(Subscription.objects.filter(user=self.user).count(), 0)
        self.assertEqual(PaymentTransaction.objects.filter(user=self.user).count(), 0)

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_create_paid_subscription_invalid_plan(self, mock_paystack):
        """Test handling of invalid plan"""

        # Create a plan with invalid data (price = 0)
        invalid_plan = SubscriptionPlan(
            name="Invalid Plan",
            price=Decimal("0.00"),
            billing_cycle="MONTHLY",
            paystack_plan_code="PLN_invalid",
            features={},
        )

        # Don't save it - just pass it to the service
        # The service should handle this gracefully

        # If your service validates the plan, it should raise an error
        # If not, it will fail at the Paystack level

        with self.assertRaises(Exception):
            subscription_service.create_paid_subscription(
                user=self.user, plan=invalid_plan
            )


class VerifyAndActivateSubscriptionTestCase(APITestCase):
    """Test cases for subscription_service.verify_and_activate_subscription()"""

    def setUp(self):
        """Set up test data"""
        self.plan = SubscriptionPlan.objects.create(
            name="Premium Monthly",
            price=Decimal("5000.00"),
            billing_cycle="MONTHLY",
            paystack_plan_code="PLN_test123",
            features={"max_articles": 100},
        )
        self.user = TestUtil.verified_user()

        # Create a subscription with pending transaction
        self.subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            start_date=timezone.now(),
            reference="TXN_TEST123456",
        )

        self.pending_transaction = PaymentTransaction.objects.create(
            user=self.user,
            subscription=self.subscription,
            reference="TXN_TEST123456",
            amount=self.plan.price,
            status=StatusChoices.PENDING,
            transaction_type=TransactionTypeChoices.SUBSCRIPTION,
        )

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_verify_and_activate_subscription_success(self, mock_paystack):
        """Test successful payment verification and subscription activation"""

        # Mock Paystack verification response - more than this in the docs
        mock_paystack.verify_transaction.return_value = {
            "status": "success",
            "reference": "TXN_TEST123456",
            "amount": 500000,  # Amount in kobo (5000 NGN)
            "paid_at": "2025-12-15T10:30:00.000Z",
            "customer": {
                "email": self.user.email,
            },
        }

        success, _, payment_transaction = (
            subscription_service.verify_and_activate_subscription(
                reference="TXN_TEST123456"
            )
        )

        self.assertTrue(success)

        # Verify transaction was updated
        self.pending_transaction.refresh_from_db()
        self.assertEqual(self.pending_transaction.status, StatusChoices.SUCCESS)
        self.assertIsNotNone(self.pending_transaction.paid_at)
        self.assertEqual(self.pending_transaction.id, payment_transaction.id)

        # Should be NOne cos webhook will update it
        self.subscription.refresh_from_db()
        self.assertIsNone(self.subscription.status)
        self.assertIsNone(self.subscription.current_period_start)
        self.assertIsNone(self.subscription.current_period_end)
        self.assertIsNone(self.subscription.next_billing_date)

        # Verify Paystack was called with correct reference
        mock_paystack.verify_transaction.assert_called_once_with("TXN_TEST123456")

    def test_verify_and_activate_subscription_already_processed(self):
        """Test that already processed transactions return success without re-processing"""

        # Mark transaction as already successful
        self.pending_transaction.status = StatusChoices.SUCCESS
        self.pending_transaction.paid_at = timezone.now()
        self.pending_transaction.save()

        # Mark subscription as already active
        self.subscription.status = SubscriptionChoices.ACTIVE
        self.subscription.current_period_start = timezone.now()
        self.subscription.current_period_end = timezone.now() + timezone.timedelta(
            days=30
        )
        self.subscription.save()

        # Call the method
        success, message, _ = subscription_service.verify_and_activate_subscription(
            reference="TXN_TEST123456"
        )

        self.assertTrue(success)
        self.assertIn("Already processed", message)

    def test_verify_and_activate_subscription_transaction_not_found(self):
        """Test failure when transaction reference doesn't exist"""

        # Call with non-existent reference
        success, message, _ = subscription_service.verify_and_activate_subscription(
            reference="TXN_NONEXISTENT"
        )

        self.assertFalse(success)
        self.assertIn("Transaction not found", message)

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_verify_and_activate_subscription_paystack_verification_fails(
        self, mock_paystack
    ):
        """Test failure when Paystack verification API call fails"""

        # Mock Paystack to raise an exception
        mock_paystack.verify_transaction.side_effect = Exception(
            "Paystack API error: Connection timeout"
        )

        success, message, _ = subscription_service.verify_and_activate_subscription(
            reference="TXN_TEST123456"
        )

        self.assertFalse(success)
        print(message)

        # Verify transaction status wasn't changed
        self.pending_transaction.refresh_from_db()
        self.assertEqual(self.pending_transaction.status, StatusChoices.PENDING)

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_verify_and_activate_subscription_payment_status_not_success(
        self, mock_paystack
    ):
        """Test failure when Paystack returns non-success payment status"""

        # Mock Paystack verification response with failed status
        mock_paystack.verify_transaction.return_value = {
            "status": "failed",
            "reference": "TXN_TEST123456",
            "amount": 500000,
            "customer": {
                "email": self.user.email,
            },
        }

        # Call the method
        success, message, _ = subscription_service.verify_and_activate_subscription(
            reference="TXN_TEST123456"
        )

        # Assertions
        self.assertFalse(success)
        print(message)
        self.assertIn("Payment failed", message)

        # Verify transaction was marked as failed
        self.pending_transaction.refresh_from_db()
        self.assertEqual(self.pending_transaction.status, StatusChoices.FAILED)
        self.assertIsNotNone(self.pending_transaction.failed_at)

        # Verify subscription was NOT activated
        self.subscription.refresh_from_db()
        self.assertIsNone(self.subscription.status)


# python manage.py test apps.subscriptions.tests.VerifyAndActivateSubscriptionTestCase
# python manage.py test apps.subscriptions.tests.CreatePaidSubscriptionTestCase
# python manage.py test apps.subscriptions.tests.VerifyAndActivateSubscriptionTestCase
# python manage.py test apps.subscriptions.tests.StartTrialTestCase
