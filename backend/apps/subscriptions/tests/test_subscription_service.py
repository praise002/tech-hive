from datetime import timedelta
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


class ProcessSuccessfulPaymentTestCase(APITestCase):
    """Test cases for subscription_service.process_successful_payment()"""

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

    def test_process_successful_payment_first_payment(self):
        """Test successful first payment processing"""

        # Create subscription without status (first payment)
        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            start_date=timezone.now(),
            reference="TXN_FIRST123",
        )

        # Mock transaction data from Paystack
        transaction_data = {
            "reference": "pay_test123",
            "amount": 500000,  # 5000 NGN in kobo
            "currency": "NGN",
            "status": "success",
        }

        # period_end, start, next is handles manually in handle_subscription_create
        payment_transaction = subscription_service.process_successful_payment(
            subscription=subscription,
            transaction_data=transaction_data,
            transaction_type=TransactionTypeChoices.SUBSCRIPTION,
        )

        # Verify subscription was activated
        subscription.refresh_from_db()
        self.assertEqual(subscription.status, SubscriptionChoices.ACTIVE)

        # Verify retry tracking was reset
        self.assertEqual(subscription.retry_count, 0)
        self.assertIsNone(subscription.payment_failed_at)
        self.assertIsNone(subscription.last_retry_at)

        # Verify transaction was created
        self.assertEqual(payment_transaction.user, self.user)
        self.assertEqual(payment_transaction.subscription, subscription)
        self.assertEqual(payment_transaction.amount, Decimal("5000.00"))
        self.assertEqual(payment_transaction.status, StatusChoices.SUCCESS)
        self.assertIsNotNone(payment_transaction.paid_at)

    def test_process_successful_payment_recovery_from_past_due(self):
        """Test processing successful payment after failure"""
        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            reference="TXN_test123",
            status=SubscriptionChoices.PAST_DUE,
            payment_failed_at=timezone.now() - timedelta(days=3),
            retry_count=2,
        )

        transaction_data = {
            "reference": "TXN_retry",
            "amount": 500000,
            "currency": "NGN",
            "status": "success",
        }

        subscription_service.process_successful_payment(
            subscription=subscription,
            transaction_data=transaction_data,
            transaction_type="RENEWAL",
        )

        # Verify subscription recovered
        subscription.refresh_from_db()
        self.assertEqual(subscription.status, SubscriptionChoices.ACTIVE)
        self.assertEqual(subscription.retry_count, 0)
        self.assertIsNone(subscription.payment_failed_at)
        self.assertIsNone(subscription.last_retry_at)


class ProcessFailedPaymentTestCase(APITestCase):
    """Test cases for subscription_service.process_failed_payment()"""

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

    def test_process_failed_payment(self):
        """Test processing failed payment"""
        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            reference="TXN_test123",
            status=SubscriptionChoices.ACTIVE,
        )

        transaction = subscription_service.process_failed_payment(
            subscription=subscription, failure_reason="Insufficient funds"
        )

        # Verify transaction created
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.status, StatusChoices.FAILED)
        self.assertEqual(transaction.failure_reason, "Insufficient funds")

        # Verify subscription marked as PAST_DUE
        subscription.refresh_from_db()
        self.assertEqual(subscription.status, SubscriptionChoices.PAST_DUE)
        self.assertIsNotNone(subscription.payment_failed_at)


class RetryPaymentTestCase(APITestCase):
    """Test cases for subscription_service.retry_payment()"""

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
    def test_retry_payment_success_manual(self, mock_paystack):
        """Test manual retry success"""
        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            reference="TXN_test123",
            status=SubscriptionChoices.PAST_DUE,
            payment_failed_at=timezone.now() - timedelta(days=3),
            retry_count=1,
            paystack_authorization_code="AUTH_test123",
        )

        # Mock successful charge
        mock_paystack.charge_authorization.return_value = {
            "status": True,
            "data": {
                "reference": "pay_retry_success",
                "amount": 500000,
                "currency": "NGN",
                "status": "success",
            },
        }

        success, message, transaction = subscription_service.retry_payment(
            subscription=subscription, is_manual=True
        )
        print(success, message, transaction)

        # Verify success
        self.assertTrue(success)
        self.assertEqual(message, "Payment successful")
        self.assertIsNotNone(transaction)

        # Verify subscription recovered
        subscription.refresh_from_db()
        self.assertEqual(subscription.status, SubscriptionChoices.ACTIVE)
        # Reset on success - it is also reset to 0 by process_successful_payment
        self.assertEqual(subscription.retry_count, 0)

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_retry_payment_success_automatic(self, mock_paystack):
        """Test automatic retry success"""
        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            reference="TXN_test123",
            status=SubscriptionChoices.PAST_DUE,
            payment_failed_at=timezone.now() - timedelta(days=3),
            retry_count=1,
            paystack_authorization_code="AUTH_test123",
        )

        # Mock successful charge
        mock_paystack.charge_authorization.return_value = {
            "status": True,
            "data": {"reference": "TXN_retry", "amount": 500000, "status": "success"},
        }

        success, _, _ = subscription_service.retry_payment(
            subscription=subscription,
        )

        # Verify success
        self.assertTrue(success)

        # Reset on success
        subscription.refresh_from_db()
        self.assertEqual(subscription.retry_count, 0)

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_retry_payment_failure(self, mock_paystack):
        """Test retry failure"""
        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            reference="TXN_test123",
            status=SubscriptionChoices.PAST_DUE,
            payment_failed_at=timezone.now() - timedelta(days=3),
            retry_count=1,
            paystack_authorization_code="AUTH_test123",
        )

        # Mock failed charge
        mock_paystack.charge_authorization.return_value = {
            "status": False,
            "message": "Insufficient funds",
        }

        success, message, transaction = subscription_service.retry_payment(
            subscription=subscription,
        )

        # Verify failure
        self.assertFalse(success)
        self.assertEqual(message, "Insufficient funds")
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.status, StatusChoices.FAILED)

        # Verify retry_count incremented
        subscription.refresh_from_db()
        self.assertEqual(subscription.retry_count, 2)

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_retry_payment_not_past_due(self, mock_paystack):
        """Test retry fails if subscription not PAST_DUE"""
        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            reference="TXN_test123",
            status=SubscriptionChoices.ACTIVE,
            paystack_authorization_code="AUTH_test123",
        )

        success, message, transaction = subscription_service.retry_payment(
            subscription=subscription, is_manual=True
        )

        # Verify failure
        self.assertFalse(success)
        self.assertIn("not past due", message.lower())
        self.assertIsNone(transaction)
        # Paystack should not be called
        mock_paystack.charge_authorization.assert_not_called()

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_retry_payment_no_authorization_code(self, mock_paystack):
        """Test retry fails if no saved payment method"""
        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            reference="TXN_test123",
            status=SubscriptionChoices.PAST_DUE,
            payment_failed_at=timezone.now() - timedelta(days=3),
            paystack_authorization_code=None,
        )

        success, message, transaction = subscription_service.retry_payment(
            subscription=subscription, is_manual=True
        )

        # Verify failure
        self.assertFalse(success)
        self.assertIn("No saved payment method", message)
        self.assertIsNone(transaction)


class CancelSubscriptionTestCase(APITestCase):
    """Test cases for subscription_service.cancel_subscription()"""

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
    @patch("apps.subscriptions.services.subscription_service.notification_service")
    def test_cancel_subscription_success(self, mock_notification, mock_paystack):
        """Test successful cancellation"""
        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            reference="TXN_test123",
            status=SubscriptionChoices.ACTIVE,
            paystack_subscription_code="SUB_test123",
            paystack_email_token="token123",
            current_period_end=timezone.now() + timedelta(days=20),
        )

        # Mock Paystack disable success
        mock_paystack.disable_subscription.return_value = True

        success = subscription_service.cancel_subscription(
            subscription=subscription, reason="Too expensive"
        )

        # Verify success
        self.assertTrue(success)

        # Verify subscription cancelled
        subscription.refresh_from_db()
        self.assertEqual(subscription.status, SubscriptionChoices.CANCELLED)
        self.assertIsNotNone(subscription.cancelled_at)
        self.assertEqual(subscription.cancel_reason, "Too expensive")
        self.assertTrue(subscription.cancel_at_period_end)
        self.assertFalse(subscription.auto_renew)

        # Verify Paystack called
        mock_paystack.disable_subscription.assert_called_once_with(
            subscription_code="SUB_test123", email_token="token123"
        )
        mock_notification.send_cancellation_confirmed_email.assert_called_once()

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_cancel_subscription_paystack_fails(self, mock_paystack):
        """Test cancellation when Paystack fails"""
        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            reference="TXN_test123",
            status=SubscriptionChoices.ACTIVE,
            paystack_subscription_code="SUB_test123",
            paystack_email_token="token123",
        )

        # Mock Paystack disable failure
        mock_paystack.disable_subscription.side_effect = Exception("Paystack error")

        success = subscription_service.cancel_subscription(subscription=subscription)

        # Verify failure
        self.assertFalse(success)

        # Verify subscription not cancelled
        subscription.refresh_from_db()
        self.assertEqual(subscription.status, SubscriptionChoices.ACTIVE)
        self.assertIsNone(subscription.cancelled_at)

    def test_cancel_subscription_already_cancelled(self):
        """Test cancelling already cancelled subscription raises error"""

        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            status=SubscriptionChoices.CANCELLED,
            reference="TXN_ALREADYCANCEL123",
        )

        with self.assertRaises(ValueError) as context:
            subscription_service.cancel_subscription(subscription=subscription)

        self.assertIn("already cancelled", str(context.exception))

    def test_cancel_subscription_expired(self):
        """Test cancelling expired subscription raises error"""

        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            status=SubscriptionChoices.EXPIRED,
            reference="TXN_EXPIRED123",
        )

        with self.assertRaises(ValueError) as context:
            subscription_service.cancel_subscription(subscription=subscription)

        self.assertIn("expired", str(context.exception).lower())


class ReactivateSubscriptionTestCase(APITestCase):
    """Test cases for subscription_service.reactivate_subscription()"""

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
    @patch("apps.subscriptions.services.subscription_service.notification_service")
    def test_reactivate_subscription_success(self, mock_notification, mock_paystack):
        """Test successful reactivation"""
        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            reference="TXN_test123",
            status=SubscriptionChoices.CANCELLED,
            cancelled_at=timezone.now() - timedelta(days=1),
            cancel_at_period_end=True,
            current_period_end=timezone.now() + timedelta(days=20),
            paystack_subscription_code="SUB_test123",
            paystack_email_token="token123",
        )

        # Mock Paystack enable success
        mock_paystack.enable_subscription.return_value = True

        success = subscription_service.reactivate_subscription(subscription)

        # Verify success
        self.assertTrue(success)

        # Verify subscription reactivated
        subscription.refresh_from_db()
        self.assertEqual(subscription.status, SubscriptionChoices.ACTIVE)
        self.assertIsNone(subscription.cancelled_at)
        self.assertFalse(subscription.cancel_at_period_end)
        self.assertTrue(subscription.auto_renew)

        mock_notification.send_reactivation_email.assert_called_once()

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_reactivate_subscription_not_cancelled(self, mock_paystack):
        """Test reactivation fails if not cancelled"""
        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            reference="TXN_test123",
            status=SubscriptionChoices.ACTIVE,
        )

        with self.assertRaises(ValueError) as context:
            subscription_service.reactivate_subscription(subscription)

        self.assertIn("only reactivate cancelled", str(context.exception).lower())

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_reactivate_subscription_period_ended(self, mock_paystack):
        """Test reactivation fails if period ended"""
        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            reference="TXN_test123",
            status=SubscriptionChoices.CANCELLED,
            cancelled_at=timezone.now() - timedelta(days=10),
            current_period_end=timezone.now() - timedelta(days=1),
        )

        with self.assertRaises(ValueError) as context:
            subscription_service.reactivate_subscription(subscription)

        self.assertIn("period has ended", str(context.exception).lower())

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_reactivate_subscription_paystack_fails(self, mock_paystack):
        """Test reactivation when Paystack enable fails"""

        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            status=SubscriptionChoices.CANCELLED,
            paystack_subscription_code="SUB_test123",
            paystack_email_token="token_test123",
            current_period_end=timezone.now() + timezone.timedelta(days=15),
            reference="TXN_PAYSTACKFAIL123",
        )

        # Mock Paystack failure
        mock_paystack.enable_subscription.side_effect = Exception("Paystack API error")

        result = subscription_service.reactivate_subscription(subscription=subscription)

        self.assertFalse(result)

        # Subscription should NOT be reactivated in our DB
        subscription.refresh_from_db()
        self.assertEqual(subscription.status, SubscriptionChoices.CANCELLED)


class UpdatePaymentMethodTestCase(APITestCase):
    """Test cases for subscription_service.update_payment_method()"""

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
    def test_update_payment_method_success(self, mock_paystack):
        """Test successful payment method update link generation"""

        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            status=SubscriptionChoices.ACTIVE,
            paystack_subscription_code="SUB_test123",
            reference="TXN_UPDATE123",
        )

        # Mock Paystack response
        mock_paystack.generate_update_subscription_link.return_value = (
            "https://paystack.com/manage/update/card/link"
        )

        # Call update method
        update_link = subscription_service.update_payment_method(
            subscription=subscription
        )

        # Assertions
        self.assertEqual(update_link, "https://paystack.com/manage/update/card/link")

        # Verify Paystack was called
        mock_paystack.generate_update_subscription_link.assert_called_once_with(
            "SUB_test123"
        )

    def test_update_payment_method_no_subscription_code(self):
        """Test failure when no Paystack subscription code"""

        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            status=SubscriptionChoices.ACTIVE,
            paystack_subscription_code=None,  # No code
            reference="TXN_NOCODE123",
        )

        with self.assertRaises(ValueError) as context:
            subscription_service.update_payment_method(subscription=subscription)

        self.assertIn("No Paystack subscription", str(context.exception))

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_update_payment_method_paystack_fails(self, mock_paystack):
        """Test failure when Paystack API fails"""

        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            status=SubscriptionChoices.ACTIVE,
            paystack_subscription_code="SUB_test123",
            reference="TXN_FAIL123",
        )

        # Mock Paystack failure
        mock_paystack.generate_update_subscription_link.side_effect = Exception(
            "API error"
        )

        with self.assertRaises(Exception) as context:
            subscription_service.update_payment_method(subscription=subscription)

        self.assertIn("Failed to generate payment update link", str(context.exception))


class CreatePlanTestCase(APITestCase):
    """Test cases for subscription_service.create_plan()"""

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_create_plan_success(self, mock_paystack):
        """Test successful plan creation"""

        # Mock Paystack response
        mock_paystack.create_plan.return_value = {
            "plan_code": "PLN_abc123",
            "name": "Test Plan",
            "amount": 500000,
            "interval": "monthly",
        }

        plan = subscription_service.create_plan(
            name="Test Plan",
            interval="monthly",
            amount=5000,
            features={"test": True},
            description="Test description",
        )

        # Assertions
        self.assertIsNotNone(plan)
        self.assertEqual(plan.name, "Test Plan")
        self.assertEqual(plan.price, Decimal("5000"))
        self.assertEqual(plan.paystack_plan_code, "PLN_abc123")

        # Verify Paystack was called
        mock_paystack.create_plan.assert_called_once()

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_create_plan_paystack_creation_fails(self, mock_paystack):
        """Test that plan is not created locally if Paystack fails"""

        # Mock Paystack failure
        mock_paystack.create_plan.side_effect = Exception("Paystack API error")

        with self.assertRaises(Exception) as context:
            subscription_service.create_plan(
                name="Test Plan",
                interval="monthly",
                amount=10000,
                features={},
            )

        self.assertIn("Failed to create plan", str(context.exception))

        # Verify no plan was created in DB
        self.assertEqual(SubscriptionPlan.objects.count(), 0)


class UpdatePlanTestCase(APITestCase):
    """Test cases for subscription_service.update_plan()"""

    def setUp(self):
        """Set up test data"""
        self.plan = SubscriptionPlan.objects.create(
            name="Original Plan",
            price=Decimal("5000.00"),
            billing_cycle="monthly",
            paystack_plan_code="PLN_test123",
            features={},
        )

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_update_plan_success(self, mock_paystack):
        """Test successful plan update"""

        # Mock successful Paystack update
        mock_paystack.update_plan.return_value = {"status": True}

        updated_plan = subscription_service.update_plan(
            plan=self.plan,
            data={
                "name": "Updated Plan",
                "amount": 7000,
                "description": "New description",
            },
        )

        # Assertions
        self.assertEqual(updated_plan.name, "Updated Plan")
        self.assertEqual(updated_plan.price, Decimal("7000"))

        # Verify Paystack was called with correct data
        mock_paystack.update_plan.assert_called_once()
        call_args = mock_paystack.update_plan.call_args[1]
        self.assertEqual(call_args["plan_code"], "PLN_test123")
        self.assertEqual(call_args["data"]["amount"], 700000)  # In kobo

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_update_plan_paystack_update_fails(self, mock_paystack):
        """Test that plan is not updated locally if Paystack fails"""

        # Mock Paystack failure
        mock_paystack.update_plan.side_effect = Exception("Paystack API error")

        with self.assertRaises(Exception) as context:
            subscription_service.update_plan(
                plan=self.plan,
                data={"name": "New Name"},
            )

        self.assertIn("Failed to update plan", str(context.exception))

        # Verify plan was NOT updated in DB
        self.plan.refresh_from_db()
        self.assertEqual(self.plan.name, "Original Plan")


class FetchSubscriptionDetailsTestCase(APITestCase):
    """Test cases for subscription_service.fetch_subscription_details()"""

    def setUp(self):
        """Set up test data"""
        self.plan = SubscriptionPlan.objects.create(
            name="Premium Monthly",
            price=Decimal("5000.00"),
            billing_cycle="MONTHLY",
            paystack_plan_code="PLN_test123",
            features={},
        )
        self.user = TestUtil.verified_user()

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_fetch_subscription_details_success(self, mock_paystack):
        """Test successful subscription details fetch"""

        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            status=SubscriptionChoices.ACTIVE,
            paystack_subscription_code="SUB_test123",
            reference="TXN_FETCH123",
        )

        # Mock Paystack response
        mock_paystack.fetch_subscription.return_value = {
            "subscription_code": "SUB_test123",
            "status": "active",
            "amount": 500000,
            "next_payment_date": "2025-01-15T00:00:00.000Z",
        }

        details = subscription_service.fetch_subscription_details(subscription)

        # Assertions
        self.assertIsNotNone(details)
        self.assertEqual(details["subscription_code"], "SUB_test123")
        self.assertEqual(details["status"], "active")

        # Verify Paystack was called
        mock_paystack.fetch_subscription.assert_called_once_with("SUB_test123")

    def test_fetch_subscription_details_no_subscription_code(self):
        """Test fetch fails if no Paystack subscription code"""

        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            status=SubscriptionChoices.ACTIVE,
            paystack_subscription_code=None,
            reference="TXN_NOCODE123",
        )

        with self.assertRaises(ValueError) as context:
            subscription_service.fetch_subscription_details(subscription)

        self.assertIn("no Paystack code", str(context.exception))

    @patch("apps.subscriptions.services.subscription_service.paystack_service")
    def test_fetch_subscription_details_paystack_fails(self, mock_paystack):
        """Test fetch when Paystack API fails"""

        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            status=SubscriptionChoices.ACTIVE,
            paystack_subscription_code="SUB_test123",
            reference="TXN_FAIL123",
        )

        # Mock Paystack failure
        mock_paystack.fetch_subscription.side_effect = Exception("API error")

        with self.assertRaises(Exception) as context:
            subscription_service.fetch_subscription_details(subscription)

        self.assertIn("Failed to fetch subscription details", str(context.exception))
