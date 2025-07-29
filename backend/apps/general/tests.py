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
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Newsletter.objects.filter(email="testuser@example.com").exists()
        )

    def test_newsletter_unsubscription(self):
        # First, subscribe
        Newsletter.objects.create(email="testuser@example.com")
        # Unsubscribe using query param
        print(self.newsletter_url)
        response = self.client.delete(
            f"{self.newsletter_url}?email=testuser@example.com"
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            Newsletter.objects.filter(email="testuser@example.com").exists()
        )

        # non-existent email
        response = self.client.delete(
            f"{self.newsletter_url}?email=notfound@example.com"
        )
        self.assertEqual(response.status_code, 422)

        # no email
        response = self.client.delete(f"{self.newsletter_url}?email=")

        self.assertEqual(response.status_code, 422)


# python manage.py test apps.general.tests.TestGeneral.test_message_create
