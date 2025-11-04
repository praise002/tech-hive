from apps.common.utils import TestUtil
from apps.notification.models import Notification
from rest_framework import status
from rest_framework.test import APITestCase


class TestNotifications(APITestCase):
    url = "/api/v1/notifications/"

    def setUp(self):
        self.user1 = TestUtil.verified_user()
        self.user2 = TestUtil.other_verified_user()
        self.user3 = TestUtil.another_verified_user()

        # Create notifications for user1
        Notification.objects.create(
            recipient=self.user1, actor=self.user2, verb="commented on your post"
        )
        Notification.objects.create(
            recipient=self.user1,
            actor=self.user3,
            verb="mentioned you in a comment",
            is_read=True,
        )

        # Create a notification for user2 (should not be seen by user1)
        Notification.objects.create(
            recipient=self.user2, actor=self.user1, verb="replied to your thread"
        )

    def test_get_notifications_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_notifications_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # User1 should have exactly 2 notifications
        self.assertEqual(len(response.data["data"]["results"]), 2)

    def test_notification_for_user_with_no_notifications(self):
        self.client.force_authenticate(user=self.user3)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]["results"]), 0)


# python manage.py test apps.notification.tests.TestNotifications.test_notification_for_user_with_no_notifications
