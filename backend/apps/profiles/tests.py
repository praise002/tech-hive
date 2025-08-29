from apps.accounts.models import User
from apps.common.utils import TestUtil
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase


class TestProfiles(APITestCase):
    profile_url = "/api/v1/profiles/me/"
    profile_detail_url = "/api/v1/profiles/<str:username>/"
    avatar_update_url = "/api/v1/profiles/avatar/"

    def setUp(self):
        self.user1 = TestUtil.verified_user()
        self.user2 = TestUtil.other_verified_user()

    def test_profile(self):

        # Test successful retrieval for authenticated users
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

        user1 = User.objects.get(id=response.data["data"]["id"])
        self.assertEqual(str(user1.id), str(self.user1.id))

        # Test you can only retrieve your own profile
        # Switch to user2 and verify they get their own profile
        self.client.force_authenticate(user=self.user2)

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

        user2 = User.objects.get(id=response.data["data"]["id"])
        self.assertEqual(str(user2.id), str(self.user2.id))

        # Test 401 for unauthorized user
        self.client.force_authenticate(user=None)

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 401)

    def test_profile_detail_get(self):
        username = self.user1.username

        # Authenticated User
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(
            self.profile_detail_url.replace("<str:username>", username)
        )
        self.assertEqual(response.status_code, 200)

        # Unauthenticated User
        self.client.force_authenticate(user=None)
        response = self.client.get(
            self.profile_detail_url.replace("<str:username>", username)
        )
        self.assertEqual(response.status_code, 200)

    def test_avatar_update(self):
        # Test success

        self.client.force_authenticate(user=self.user1)

        image_content = b"GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
        image = SimpleUploadedFile(
            "test_image.gif", image_content, content_type="image/gif"
        )

        response = self.client.patch(
            self.avatar_update_url, {"avatar": image}, format="multipart"
        )

        self.assertEqual(response.status_code, 200)
        self.user1.refresh_from_db()
        self.assertTrue(self.user1.avatar)

        # Test 401 for unauthenticated users
        self.client.force_authenticate(user=None)

        response = self.client.patch(
            self.avatar_update_url, {"avatar": image}, format="multipart"
        )

        self.assertEqual(response.status_code, 401)

# python manage.py test apps.profiles.tests.TestProfiles