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

    def test_get_notification_detail_authenticated(self):
        """Test retrieving a single notification and auto-marking as read."""
        notification = Notification.objects.create(
            recipient=self.user1, actor=self.user2, verb="liked your comment"
        )
        self.assertFalse(notification.is_read)

        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f"/api/v1/notifications/{notification.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["data"]["is_read"])

        notification.refresh_from_db()
        self.assertTrue(notification.is_read)

    def test_delete_notification_authenticated(self):
        """Test soft-deleting a notification."""
        notification = Notification.objects.create(
            recipient=self.user1, actor=self.user2, verb="disliked your comment"
        )

        self.client.force_authenticate(user=self.user1)
        response = self.client.get(
            f"/api/v1/notifications/{notification.id}/"
        )  # Mark as read first to be sure
        response = self.client.delete(f"/api/v1/notifications/{notification.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify soft-delete
        notification.refresh_from_db()
        self.assertTrue(notification.is_deleted)

        # Should not be returned by default manager
        self.assertFalse(Notification.objects.filter(id=notification.id).exists())

    def test_restore_notification_authenticated(self):
        """Test restoring a soft-deleted notification."""
        notification = Notification.objects.create(
            recipient=self.user1, actor=self.user2, verb="super-liked your comment"
        )
        notification.delete()  # Soft delete
        self.assertTrue(notification.is_deleted)

        self.client.force_authenticate(user=self.user1)
        response = self.client.post(f"/api/v1/notifications/{notification.id}/restore/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["id"], str(notification.id))

        # Verify in DB
        notification.refresh_from_db()
        self.assertFalse(notification.is_deleted)
        self.assertIsNone(notification.deleted_at)

    def test_notification_security(self):
        """Test that users cannot access others' notifications."""
        notification = Notification.objects.create(
            recipient=self.user2, actor=self.user1, verb="private action"
        )

        self.client.force_authenticate(user=self.user1)

        # Try GET
        response = self.client.get(f"/api/v1/notifications/{notification.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try DELETE
        response = self.client.delete(f"/api/v1/notifications/{notification.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Try RESTORE
        response = self.client.post(f"/api/v1/notifications/{notification.id}/restore/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# python manage.py test apps.notification.tests.TestNotifications
