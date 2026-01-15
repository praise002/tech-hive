from apps.general.models import Newsletter
from rest_framework.test import APITestCase


class TestGeneral(APITestCase):
    site_detail_url = "/api/v1/site-detail/"
    newsletter_url = "/api/v1/newsletter/"
    contact_url = "/api/v1/contact/"

    def test_site_detail(self):
        # Test successful retrieval of site detail
        response = self.client.get(self.site_detail_url)

        self.assertEqual(response.status_code, 200)

    def test_contact_create(self):
        # Test successful creation
        valid_data = {
            "name": "Test User",
            "email": "test@example.com",
            "content": "This is a test message",
        }
        response = self.client.post(self.contact_url, valid_data)
        self.assertEqual(response.status_code, 201)

        # Test 422 response for missing required field
        invalid_data = {"name": "Test User", "email": "test@example.com"}
        response = self.client.post(self.contact_url, invalid_data)
        self.assertEqual(response.status_code, 422)

        # Test 422 response for invalid email format
        invalid_email_data = {
            "name": "Test User",
            "email": "not-an-email",
            "text": "This is a test message",
        }
        response = self.client.post(self.contact_url, invalid_email_data)
        self.assertEqual(response.status_code, 422)

    def test_newsletter_subscription(self):
        data = {"email": "testuser@example.com"}
        response = self.client.post(self.newsletter_url, data)
        print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Newsletter.objects.filter(
                email="testuser@example.com", is_subscribed=True
            ).exists()
        )

    def test_newsletter_duplicate_subscription_fails(self):
        email = "testuser@example.com"
        Newsletter.objects.create(email=email)

        data = {"email": email}
        response = self.client.post(self.newsletter_url, data)
        print(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertIn(
            "This email is already subscribed to the newsletter.",
            response.data["data"]["email"],
        )

    def test_newsletter_resubscription_success(self):
        email = "testuser@example.com"
        # Create an unsubscribed user
        Newsletter.objects.create(email=email, is_subscribed=False)

        data = {"email": email}
        response = self.client.post(self.newsletter_url, data)
        print(response.data)
        self.assertEqual(response.status_code, 201)

        # Verify they are now subscribed
        newsletter = Newsletter.objects.get(email=email)
        self.assertTrue(newsletter.is_subscribed)
        self.assertIsNone(newsletter.unsubscribed_at)

    def test_newsletter_unsubscription(self):
        newsletter = Newsletter.objects.create(email="testuser@example.com")
        token = newsletter.unsubscribe_token

        # Unsubscribe using the token
        response = self.client.get(f"/api/v1/newsletter/unsubscribe/{token}/")
        print(response.data)
        self.assertEqual(response.status_code, 200)

        newsletter.refresh_from_db()
        self.assertFalse(newsletter.is_subscribed)
        self.assertIsNotNone(newsletter.unsubscribed_at)

        # Invalid token
        response = self.client.get("/api/v1/newsletter/unsubscribe/invalid-token/")
        self.assertEqual(response.status_code, 404)
        print(response.data)


# python manage.py test apps.general.tests.TestGeneral.test_message_create
