import hashlib
import hmac
import logging
from decimal import Decimal
from typing import Any, Dict, Optional

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class PaystackService:
    """
    Handles all interactions with Paystack API.

    Documentation: https://paystack.com/docs/api/
    """

    def __init__(self):
        self.secret_key = settings.PAYSTACK_SECRET_KEY
        self.public_key = settings.PAYSTACK_PUBLIC_KEY
        self.base_url = "https://api.paystack.co"
        self.headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }

    def create_plan(
        self,
        name: str,
        interval: str,
        amount: int,
        currency: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a subscription plan on Paystack.

        Args:
            name: Plan name (e.g., "Premium Monthly")
            interval: Billing interval - hourly, daily, weekly, monthly, quarterly, biannually (every 6 months) and annually
            amount: Amount in naira (will be converted to kobo)
            description: Plan description (optional)
            currency: Currency code (default: NGN)
        Returns:
            {
                "name": "Monthly Retainer",
                "interval": "monthly",
                "amount": 500000,
                "integration": 428626,
                "domain": "test",
                "currency": "NGN",
                "plan_code": "PLN_u4cqud8vabi89hx",
                "invoice_limit": 0,
                "send_invoices": true,
                "send_sms": true,
                "hosted_page": false,
                "migrate": false,
                "id": 49122,
                "createdAt": "2020-05-22T12:36:12.333Z",
                "updatedAt": "2020-05-22T12:36:12.333Z"
                }
        Raises:
            Exception: If plan creation fails
        """
        try:
            # Convert amount to kobo
            amount_in_kobo = int(amount * Decimal("100"))

            payload = {
                "name": name,
                "interval": interval,
                "amount": amount_in_kobo,
            }

            if description:
                payload["description"] = description

            if currency:
                payload["currency"] = currency

            logger.info(f"Creating Paystack plan: {name} - ₦{amount}/{interval}")

            response = requests.post(
                f"{self.base_url}/plan",
                json=payload,
                headers=self.headers,
                timeout=30,
            )

            response.raise_for_status()
            data = response.json()

            if not data.get("status"):
                error_message = data.get("message", "Plan creation failed")
                logger.error(f"Failed to create plan: {error_message}")
                raise Exception(f"Paystack error: {error_message}")

            plan_data = data["data"]
            logger.info(f"Plan created successfully: {plan_data['plan_code']}")

            return plan_data

        except requests.exceptions.RequestException as e:
            logger.error(f"Paystack API request failed: {str(e)}")
            raise Exception(f"Failed to connect to Paystack: {str(e)}")

        except Exception as e:
            logger.error(f"Error creating plan: {str(e)}")
            raise

    def update_plan(self, plan_code: str, data: Dict) -> Dict:
        """
        Updates the details of a subscription plan on Paystack.

        Args:
            plan_code: The ID or code of the plan to update.
            data: A dictionary containing the fields to update.
                  e.g., {"name": "New Name", "amount": 55000, "update_existing_subscriptions": True} this is True by default
                  Amount should be in the subunit (kobo).

        Returns:
            The response dictionary from Paystack.

        Raises:
            Exception: If the update fails.
        """
        try:
            url = f"{self.base_url}/plan/{plan_code}"
            logger.info(f"Updating plan '{plan_code}' with data: {data}")

            response = requests.put(
                url,
                headers=self.headers,
                json=data,
                timeout=30,
            )

            response.raise_for_status()
            response_data = response.json()

            if not response_data.get("status"):
                error_message = response_data.get("message", "Failed to update plan")
                logger.error(f"Failed to update plan '{plan_code}': {error_message}")
                raise Exception(error_message)

            logger.info(
                f"Plan '{plan_code}' updated successfully: {response_data.get('message')}"
            )
            return response_data

        except requests.exceptions.RequestException as e:
            logger.error(
                f"Paystack API request failed while updating plan '{plan_code}': {str(e)}"
            )
            raise Exception(f"Failed to connect to Paystack: {str(e)}")
        except Exception as e:
            logger.error(f"Error updating plan '{plan_code}': {str(e)}")
            raise

    def list_plans(
        self,
        page: int = 1,
        per_page: int = 50,
        status: Optional[str] = None,
        interval: Optional[str] = None,
        amount: Optional[Decimal] = None,
    ) -> Dict[str, Any]:
        """
        List all subscription plans on your Paystack integration.

        Args:
            page: Page number for pagination (default: 1)
            per_page: Number of plans per page (default: 50, max: 100)
            status: Filter by plan status (optional) - e.g., "active"
            interval: Filter by billing interval (optional) - e.g., "monthly", "annually"
            amount: Filter by plan amount in Naira (optional)

        Returns:
            {
                "plans": [ ... ],
                "meta": { ... }
            }

        Raises:
            Exception: If API call fails
        """
        try:
            # Build query parameters
            params = {
                "page": page,
                "perPage": per_page,
            }

            if status:
                params["status"] = status

            if interval:
                params["interval"] = interval

            if amount:
                # Convert amount to kobo
                params["amount"] = int(amount * Decimal("100"))

            logger.info(
                f"Fetching plans (page {page}, per_page {per_page}, "
                f"status={status}, interval={interval}, amount={amount})"
            )

            response = requests.get(
                f"{self.base_url}/plan",
                headers=self.headers,
                params=params,
                timeout=30,
            )

            response.raise_for_status()
            data = response.json()

            if not data.get("status"):
                error_message = data.get("message", "Failed to list plans")
                logger.error(f"Failed to list plans: {error_message}")
                raise Exception(f"Paystack error: {error_message}")

            plans_data = data["data"]
            meta = data.get("meta", {})

            logger.info(
                f"Retrieved {len(plans_data)} plans (total: {meta.get('total', 0)})"
            )

            return {
                "plans": plans_data,
                "meta": meta,
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Paystack API request failed: {str(e)}")
            raise Exception(f"Failed to connect to Paystack: {str(e)}")

        except Exception as e:
            logger.error(f"Error listing plans: {str(e)}")
            raise

    def fetch_plan(self, id_or_code: str) -> Dict[str, Any]:
        """
        Fetch details of a specific plan on your integration.

        Args:
            id_or_code: The plan ID or plan_code (e.g., "PLN_gx2wn530m0i3w3m" or "28")

        Returns:
            {
                "subscriptions": [],
                "integration": 100032,
                "domain": "test",
                "name": "Monthly retainer",
                "plan_code": "PLN_gx2wn530m0i3w3m",
                "description": null,
                "amount": 50000,  # in kobo
                "interval": "monthly",
                "send_invoices": true,
                "send_sms": true,
                "currency": "NGN",
                "id": 28,
                "createdAt": "2016-03-29T22:42:50.000Z",
                "updatedAt": "2016-03-29T22:42:50.000Z"
            }

        Raises:
            Exception: If plan fetch fails
        """
        try:
            logger.info(f"Fetching plan: {id_or_code}")

            response = requests.get(
                f"{self.base_url}/plan/{id_or_code}",
                headers=self.headers,
                timeout=30,
            )

            response.raise_for_status()
            data = response.json()

            if not data.get("status"):
                error_message = data.get("message", "Failed to fetch plan")
                logger.error(f"Failed to fetch plan '{id_or_code}': {error_message}")
                raise Exception(f"Paystack error: {error_message}")

            plan_data = data["data"]
            logger.info(
                f"Plan '{id_or_code}' retrieved successfully: {plan_data['name']}"
            )

            return plan_data

        except requests.exceptions.RequestException as e:
            logger.error(f"Paystack API request failed: {str(e)}")
            raise Exception(f"Failed to connect to Paystack: {str(e)}")

        except Exception as e:
            logger.error(f"Error fetching plan '{id_or_code}': {str(e)}")
            raise

    def initialize_transaction(
        self,
        email: str,
        amount: str,
        plan_code: str,
        callback_url: Optional[str] = None,
        metadata: Optional[Dict] = None,
        reference: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Initialize a Paystack transaction.

        Args:
            email: Customer email
            amount: Amount in Naira (will be converted to kobo)
            plan_code: Paystack plan code (for subscriptions)- will override transaction amount passed
            callback_url: URL to redirect after payment
            metadata: Additional data to attach
            reference: Custom reference (optional)
        Returns:
            {
                "authorization_url": "https://checkout.paystack.com/nkdks46nymizns7",
                "access_code": "nkdks46nymizns7",
                "reference": "nms6uvr1pl"  # REFRENCE NOT PASSED, PAYSTACK RETURNS A REFRENCE, REFRENCE PASSED NOT SURE IF PAYSTACK RETURNS MINE
            }

        Raises:
            Exception: If API call fails
        """
        try:
            # Convert amount to kobo (Paystack uses kobo)
            amount_in_kobo = int(amount * Decimal("100"))

            payload = {
                "email": email,
                "amount": amount_in_kobo,
                "plan": plan_code,  # it invalidates the value provided in amount
            }

            if callback_url:
                payload["callback_url"] = callback_url

            if metadata:
                payload["metadata"] = metadata

            if reference:
                payload["reference"] = reference

            logger.info(f"Initializing Paystack transaction for {email}: ₦{amount}")

            response = requests.post(
                f"{self.base_url}/transaction/initialize",
                json=payload,
                headers=self.headers,
                timeout=30,
            )

            response.raise_for_status()
            data = response.json()

            if not data.get("status"):
                error_message = data.get("message", "Unknown error")
                logger.error(f"Paystack initialization failed: {error_message}")
                raise Exception(f"Paystack error: {error_message}")

            result = data["data"]
            logger.info(f"Transaction initialized successfully: {result['reference']}")

            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"Paystack API request failed: {str(e)}")
            raise Exception(f"Failed to connect to Paystack: {str(e)}")

        except Exception as e:
            logger.error(f"Error initializing transaction: {str(e)}")
            raise

    def verify_transaction(self, reference: str) -> Dict[str, Any]:
        """
        Verify a transaction.

        Args:
            reference: Transaction reference

        Returns:
            Full transaction data from Paystack

        Raises:
            Exception: If verification fails
        """
        try:
            logger.info(f"Verifying transaction: {reference}")

            response = requests.get(
                f"{self.base_url}/transaction/verify/{reference}",
                headers=self.headers,
                timeout=30,
            )

            response.raise_for_status()
            data = response.json()

            if not data.get("status"):
                error_message = data.get("message", "Verification failed")
                logger.error(f"Transaction verification failed: {error_message}")
                raise Exception(f"Verification error: {error_message}")

            transaction_data = data["data"]
            status = transaction_data.get("status")

            logger.info(f"Transaction {reference} verified: {status}")

            return transaction_data

        except requests.exceptions.RequestException as e:
            logger.error(f"Paystack API request failed: {str(e)}")
            raise Exception(f"Failed to verify transaction: {str(e)}")

        except Exception as e:
            logger.error(f"Error verifying transaction: {str(e)}")
            raise

    def charge_authorization(
        self,
        authorization_code: str,
        email: str,
        amount: str,
        metadata: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Charge an existing authorization.
        You manually handle renewals.

        Args:
            authorization_code: Authorization code from previous transaction
            email: Customer email
            amount: Amount in Naira
            metadata: Additional data

        Returns:
            Transaction data

        Raises:
            Exception: If charge fails
        """
        try:
            amount_in_kobo = str(
                amount * Decimal("100")
            )  # in subunit of supported currency

            payload = {
                "authorization_code": authorization_code,
                "email": email,
                "amount": amount_in_kobo,
            }

            if metadata:
                payload["metadata"] = metadata

            logger.info(f"Charging authorization for {email}: ₦{amount}")

            response = requests.post(
                f"{self.base_url}/transaction/charge_authorization",
                json=payload,
                headers=self.headers,
                timeout=30,
            )

            response.raise_for_status()
            data = response.json()

            if not data.get("status"):
                error_message = data.get("message", "Charge failed")
                logger.warning(f"Authorization charge failed: {error_message}")
                # Don't raise exception - return the response so we can handle failure
                return data

            transaction_data = data["data"]
            logger.info(
                f"Authorization charged successfully: {transaction_data['reference']}"
            )

            return data

        except requests.exceptions.RequestException as e:
            logger.error(f"Paystack API request failed: {str(e)}")
            return {
                "status": False,
                "message": f"Network error: {str(e)}",
                "data": None,
            }

        except Exception as e:
            logger.error(f"Error charging authorization: {str(e)}")
            return {"status": False, "message": str(e), "data": None}

    def create_subscription(
        self,
        customer_code: str,
        plan_code: str,
        authorization_code: str,
        start_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a subscription directly (after card authorization).
        Paystack manages renewals.

        Args:
            customer_code: Paystack customer code
            plan_code: Paystack plan code
            authorization_code: Card authorization code
            start_date: ISO 8601 format (optional)
            start_date parameter, which lets you set the date for the first debit.
            This makes this method useful for situations where you'd like to give a customer a free period before you start charging them,
            or when you want to switch a customer to a different plan.
        Returns:
            Subscription data
        """
        try:
            payload = {
                "customer": customer_code,
                "plan": plan_code,
                "authorization": authorization_code,
            }

            if start_date:
                payload["start_date"] = start_date

            logger.info(f"Creating Paystack subscription for customer {customer_code}")

            response = requests.post(
                f"{self.base_url}/subscription",
                json=payload,
                headers=self.headers,
                timeout=30,
            )

            response.raise_for_status()
            data = response.json()

            if not data.get("status"):
                error_message = data.get("message", "Subscription creation failed")
                logger.error(f"Subscription creation failed: {error_message}")
                raise Exception(f"Subscription error: {error_message}")

            subscription_data = data["data"]
            logger.info(
                f"Subscription created: {subscription_data['subscription_code']}"
            )

            return subscription_data

        except Exception as e:
            logger.error(f"Error creating subscription: {str(e)}")
            raise

    def fetch_subscription(self, subscription_code_or_id: str) -> Dict[str, Any]:
        """
        Fetch subscription details.

        Args:
            subscription_code_or_id: Subscription code or ID

        Returns:
            Subscription data
        """
        try:
            response = requests.get(
                f"{self.base_url}/subscription/{subscription_code_or_id}",
                headers=self.headers,
                timeout=30,
            )

            response.raise_for_status()
            data = response.json()

            if not data.get("status"):
                raise Exception(data.get("message", "Failed to fetch subscription"))

            return data["data"]

        except Exception as e:
            logger.error(f"Error fetching subscription: {str(e)}")
            raise

    def disable_subscription(self, subscription_code: str, email_token: str) -> bool:
        """
        Disable (cancel) a subscription.

        Args:
            subscription_code: Paystack subscription code
            email_token: Email token for the subscription
            Gotten from create_subcription response

        Returns:
            True if successful
        """
        try:
            payload = {
                "code": subscription_code,
                "token": email_token,
            }

            logger.info(f"Disabling subscription: {subscription_code}")

            response = requests.post(
                f"{self.base_url}/subscription/disable",
                json=payload,
                headers=self.headers,
                timeout=30,
            )

            response.raise_for_status()
            data = response.json()

            if not data.get("status"):
                error_message = data.get("message", "Failed to disable subscription")
                logger.error(f"Failed to disable subscription: {error_message}")
                raise Exception(error_message)

            logger.info(f"Subscription disabled successfully: {subscription_code}")
            return True

        except Exception as e:
            logger.error(f"Error disabling subscription: {str(e)}")
            raise

    def enable_subscription(self, subscription_code: str, email_token: str) -> bool:
        """
        Enable (reactivate) a subscription.

        Args:
            subscription_code: Paystack subscription code
            email_token: Email token for the subscription

        Returns:
            True if successful
        """
        try:
            payload = {
                "code": subscription_code,
                "token": email_token,
            }

            logger.info(f"Enabling subscription: {subscription_code}")

            response = requests.post(
                f"{self.base_url}/subscription/enable",
                json=payload,
                headers=self.headers,
                timeout=30,
            )

            response.raise_for_status()
            data = response.json()

            if not data.get("status"):
                error_message = data.get("message", "Failed to enable subscription")
                logger.error(f"Failed to enable subscription: {error_message}")
                raise Exception(error_message)

            logger.info(f"Subscription enabled successfully: {subscription_code}")
            return True

        except Exception as e:
            logger.error(f"Error enabling subscription: {str(e)}")
            raise

    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """
        Verify that webhook came from Paystack.

        Args:
            payload: Raw request body (bytes)
            signature: x-paystack-signature header value

        Returns:
            True if signature is valid
        """
        try:
            computed_signature = hmac.new(
                self.secret_key.encode("utf-8"), payload, hashlib.sha512
            ).hexdigest()

            is_valid = hmac.compare_digest(computed_signature, signature)

            if not is_valid:
                logger.warning("Invalid webhook signature detected")

            return is_valid

        except Exception as e:
            logger.error(f"Error verifying webhook signature: {str(e)}")
            return False

    def generate_update_subscription_link(self, subscription_code: str) -> str:
        """
        Generate a link for a customer to update the card on a subscription.

        Args:
            subscription_code: The code of the subscription to generate a link for.

        Returns:
            The management link URL as a string.

        Raises:
            Exception: If link generation fails.
        """
        try:
            url = f"{self.base_url}/subscription/{subscription_code}/manage/link"
            logger.info(f"Generating update link for subscription: {subscription_code}")

            response = requests.get(
                url,
                headers=self.headers,
                timeout=30,
            )

            response.raise_for_status()
            data = response.json()

            if not data.get("status"):
                error_message = data.get("message", "Failed to generate update link")
                logger.error(f"Failed to generate update link: {error_message}")
                raise Exception(error_message)

            link = data["data"]["link"]
            logger.info(f"Update link generated successfully for {subscription_code}")

            return link

        except requests.exceptions.RequestException as e:
            logger.error(f"Paystack API request failed: {str(e)}")
            raise Exception(f"Failed to connect to Paystack: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating subscription update link: {str(e)}")
            raise


paystack_service = PaystackService()
