import uuid
from unittest.mock import patch

from apps.accounts.utils import UserRoles
from apps.common.utils import TestUtil
from apps.content.choices import ArticleStatusChoices
from apps.content.models import Article
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class LiveblocksAuthViewTests(APITestCase):
    """
    Test suite for LiveblocksAuthView endpoint.
    Tests authentication, permissions, and token generation.
    """

    def setUp(self):
        """Set up test users and articles"""

        self.author = TestUtil.verified_user()
        self.reviewer = TestUtil.another_verified_user()
        self.editor = TestUtil.other_verified_user()
        self.random_user = TestUtil.random_user()

        contributor_group, _ = Group.objects.get_or_create(name=UserRoles.CONTRIBUTOR)
        reviewer_group, _ = Group.objects.get_or_create(name=UserRoles.REVIEWER)
        editor_group, _ = Group.objects.get_or_create(name=UserRoles.EDITOR)

        self.author.groups.add(contributor_group)
        self.reviewer.groups.add(reviewer_group)
        self.editor.groups.add(editor_group)

        self.article = Article.objects.create(
            title="Test Article",
            content="Test content",
            author=self.author,
            status=ArticleStatusChoices.DRAFT,
        )

        self.url = "/api/v1/liveblocks/auth/"
        self.valid_room_id = f"article-{self.article.id}"

    def test_unauthenticated_request_returns_401(self):
        """Unauthenticated users should be denied access"""
        response = self.client.post(self.url, {"room_id": self.valid_room_id})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_missing_room_id_returns_422(self):
        """Request without room_id should return validation error"""
        self.client.force_authenticate(user=self.author)
        response = self.client.post(self.url, {})

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_invalid_room_id_format_returns_422(self):
        """Invalid room_id format should return validation error"""
        self.client.force_authenticate(user=self.author)
        response = self.client.post(self.url, {"room_id": "invalid-format"})

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_nonexistent_article_returns_422(self):
        """Request for non-existent article should return 422"""
        self.client.force_authenticate(user=self.author)
        fake_uuid = uuid.uuid4()
        response = self.client.post(self.url, {"room_id": f"article-{fake_uuid}"})

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn("Article not found", response.data.get("message", ""))

    def test_malformed_uuid_in_room_id_returns_422(self):
        """Malformed UUID in room_id should return 422"""
        self.client.force_authenticate(user=self.author)
        response = self.client.post(self.url, {"room_id": "article-not-a-uuid"})

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    @patch("apps.content.views.liveblocks.create_liveblocks_token")
    def test_author_has_write_access_when_draft(self, mock_token):
        """Author should have WRITE access to draft articles"""
        mock_token.return_value = "mock_token_123"
        self.client.force_authenticate(user=self.author)

        self.article.status = ArticleStatusChoices.DRAFT
        self.article.save()

        response = self.client.post(self.url, {"room_id": self.valid_room_id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["token"], "mock_token_123")
        self.assertEqual(response.data["message"], "Authentication successful")

        # Verify token was created with WRITE permission
        mock_token.assert_called_once()
        call_args = mock_token.call_args

        self.assertEqual(call_args[0][2], "WRITE")

    @patch("apps.content.views.liveblocks.create_liveblocks_token")
    def test_author_has_write_access_when_changes_requested(self, mock_token):
        """Author should have WRITE access when changes are requested"""
        mock_token.return_value = "mock_token_123"
        self.client.force_authenticate(user=self.author)

        self.article.status = ArticleStatusChoices.CHANGES_REQUESTED
        self.article.save()

        response = self.client.post(self.url, {"room_id": self.valid_room_id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        call_args = mock_token.call_args
        self.assertEqual(call_args[0][2], "WRITE")

    @patch("apps.content.views.liveblocks.create_liveblocks_token")
    def test_author_has_write_access_when_rejected(self, mock_token):
        """Author should have WRITE access to rejected articles"""
        mock_token.return_value = "mock_token_123"
        self.client.force_authenticate(user=self.author)

        self.article.status = ArticleStatusChoices.REJECTED
        self.article.save()

        response = self.client.post(self.url, {"room_id": self.valid_room_id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        call_args = mock_token.call_args
        self.assertEqual(call_args[0][2], "WRITE")

    @patch("apps.content.views.liveblocks.create_liveblocks_token")
    def test_author_has_read_access_when_submitted(self, mock_token):
        """Author should have READ access when article is submitted"""
        mock_token.return_value = "mock_token_123"
        self.client.force_authenticate(user=self.author)

        self.article.status = ArticleStatusChoices.SUBMITTED_FOR_REVIEW
        self.article.save()

        response = self.client.post(self.url, {"room_id": self.valid_room_id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], "Authentication successful (read-only)"
        )
        call_args = mock_token.call_args
        self.assertEqual(call_args[0][2], "READ")

    @patch("apps.content.views.liveblocks.create_liveblocks_token")
    def test_author_has_read_access_when_under_review(self, mock_token):
        """Author should have READ access when article is under review"""
        mock_token.return_value = "mock_token_123"
        self.client.force_authenticate(user=self.author)

        self.article.status = ArticleStatusChoices.UNDER_REVIEW
        self.article.save()

        response = self.client.post(self.url, {"room_id": self.valid_room_id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], "Authentication successful (read-only)"
        )
        call_args = mock_token.call_args
        self.assertEqual(call_args[0][2], "READ")

    @patch("apps.content.views.liveblocks.create_liveblocks_token")
    def test_author_has_read_access_when_ready_for_publishing(self, mock_token):
        """Author should have READ access when article is ready for publishing"""
        mock_token.return_value = "mock_token_123"
        self.client.force_authenticate(user=self.author)

        self.article.status = ArticleStatusChoices.READY
        self.article.save()

        response = self.client.post(self.url, {"room_id": self.valid_room_id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], "Authentication successful (read-only)"
        )
        call_args = mock_token.call_args
        self.assertEqual(call_args[0][2], "READ")

    @patch("apps.content.views.liveblocks.create_liveblocks_token")
    def test_author_has_read_access_when_published(self, mock_token):
        """Author should have READ access to published articles"""
        mock_token.return_value = "mock_token_123"
        self.client.force_authenticate(user=self.author)

        self.article.status = ArticleStatusChoices.PUBLISHED
        self.article.save()

        response = self.client.post(self.url, {"room_id": self.valid_room_id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], "Authentication successful (read-only)"
        )
        call_args = mock_token.call_args
        self.assertEqual(call_args[0][2], "READ")

    @patch("apps.content.views.liveblocks.create_liveblocks_token")
    def test_assigned_reviewer_has_read_access(self, mock_token):
        """Assigned reviewer should have READ access"""
        mock_token.return_value = "mock_token_123"
        self.client.force_authenticate(user=self.reviewer)

        self.article.assigned_reviewer = self.reviewer
        self.article.status = ArticleStatusChoices.UNDER_REVIEW
        self.article.save()

        response = self.client.post(self.url, {"room_id": self.valid_room_id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], "Authentication successful (read-only)"
        )
        call_args = mock_token.call_args
        self.assertEqual(call_args[0][2], "READ")

    def test_unassigned_reviewer_has_no_access(self):
        """Reviewer not assigned to article should have no access"""
        self.client.force_authenticate(user=self.reviewer)

        self.article.assigned_reviewer = None
        self.article.save()

        response = self.client.post(self.url, {"room_id": self.valid_room_id})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("don't have permission", response.data.get("message", ""))

    @patch("apps.content.views.liveblocks.create_liveblocks_token")
    def test_assigned_editor_has_read_access(self, mock_token):
        """Assigned editor should have READ access"""
        mock_token.return_value = "mock_token_123"
        self.client.force_authenticate(user=self.editor)

        self.article.assigned_editor = self.editor
        self.article.status = ArticleStatusChoices.UNDER_REVIEW
        self.article.save()

        response = self.client.post(self.url, {"room_id": self.valid_room_id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], "Authentication successful (read-only)"
        )
        call_args = mock_token.call_args
        self.assertEqual(call_args[0][2], "READ")

    def test_unassigned_editor_has_no_access(self):
        """Editor not assigned to article should have no access"""
        self.client.force_authenticate(user=self.editor)

        self.article.assigned_editor = None
        self.article.save()

        response = self.client.post(self.url, {"room_id": self.valid_room_id})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("don't have permission", response.data.get("message", ""))

    def test_random_user_has_no_access(self):
        """Random user (not author/reviewer/editor) should have no access"""
        self.client.force_authenticate(user=self.random_user)

        response = self.client.post(self.url, {"room_id": self.valid_room_id})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("don't have permission", response.data.get("message", ""))

    @patch("apps.content.views.liveblocks.create_liveblocks_token")
    def test_successful_token_generation_returns_token_and_user_id(self, mock_token):
        """Successful token generation should return token and user_id"""
        mock_token.return_value = "jwt_token_12345"
        self.client.force_authenticate(user=self.author)

        response = self.client.post(self.url, {"room_id": self.valid_room_id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["token"], "jwt_token_12345")
        self.assertEqual(response.data["data"]["user_id"], str(self.author.id))

    @patch("apps.content.views.liveblocks.create_liveblocks_token")
    def test_token_generation_failure_returns_500(self, mock_token):
        """Token generation failure should return 500 error"""
        mock_token.side_effect = Exception("Liveblocks API error")
        self.client.force_authenticate(user=self.author)

        response = self.client.post(self.url, {"room_id": self.valid_room_id})

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn(
            "Failed to generate authentication token", response.data.get("message", "")
        )


class ArticleEditorViewTestCase(APITestCase):
    """Test article editor endpoint"""

    def setUp(self):

        self.author = TestUtil.verified_user()
        self.reviewer = TestUtil.another_verified_user()
        self.editor = TestUtil.other_verified_user()
        self.random_user = TestUtil.random_user()

        contributor_group, _ = Group.objects.get_or_create(name=UserRoles.CONTRIBUTOR)
        reviewer_group, _ = Group.objects.get_or_create(name=UserRoles.REVIEWER)
        editor_group, _ = Group.objects.get_or_create(name=UserRoles.EDITOR)

        self.author.groups.add(contributor_group)
        self.reviewer.groups.add(reviewer_group)
        self.editor.groups.add(editor_group)

        # Create draft article
        self.draft_article = Article.objects.create(
            title="Draft Article",
            content="<p>Draft content</p>",
            author=self.author,
            status=ArticleStatusChoices.DRAFT,
        )

        # Create article under review
        self.review_article = Article.objects.create(
            title="Review Article",
            content="<p>Review content</p>",
            author=self.author,
            status=ArticleStatusChoices.UNDER_REVIEW,
            assigned_reviewer=self.reviewer,
            assigned_editor=self.editor,
        )

        # Create published article
        self.published_article = Article.objects.create(
            title="Published Article",
            content="<p>Published content</p>",
            author=self.author,
            status=ArticleStatusChoices.PUBLISHED,
        )

    def test_requires_authentication(self):
        """Test that endpoint requires authentication"""
        response = self.client.get(f"/api/v1/articles/{self.draft_article.id}/editor/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_article_not_found(self):
        """Test 404 for non-existent article"""
        self.client.force_authenticate(user=self.author)
        response = self.client.get("/api/v1/articles/99999/editor/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["code"], "non_existent")

    def test_draft_author_can_access(self):
        """Test that author can access their draft"""
        self.client.force_authenticate(user=self.author)
        response = self.client.get(f"/api/v1/articles/{self.draft_article.id}/editor/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["data"]["id"], str(self.draft_article.id))
        self.assertEqual(response.data["data"]["user_can_edit"], True)
        self.assertEqual(
            response.data["data"]["liveblocks_room_id"],
            f"article-{self.draft_article.id}",
        )

    def test_draft_non_author_cannot_access(self):
        """Test that non-author cannot access draft"""
        self.client.force_authenticate(user=self.random_user)
        response = self.client.get(f"/api/v1/articles/{self.draft_article.id}/editor/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["status"], "failure")
        self.assertEqual(response.data["code"], "forbidden")

    def test_review_reviewer_cannot_edit(self):
        """Test that assigned reviewer can view article under review"""
        self.client.force_authenticate(user=self.reviewer)
        response = self.client.get(f"/api/v1/articles/{self.review_article.id}/editor/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["user_can_edit"], False)
        self.assertEqual(response.data["data"]["status"], "under_review")

    def test_review_author_can_view(self):
        """Test that author can view (but not edit) article under review"""
        self.client.force_authenticate(user=self.author)
        response = self.client.get(f"/api/v1/articles/{self.review_article.id}/editor/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["user_can_edit"], False)
        self.assertEqual(response.data["data"]["status"], "under_review")

    def test_published_non_author_gets_redirect(self):
        """Test that non-author gets redirect info for published article"""
        self.client.force_authenticate(user=self.random_user)
        response = self.client.get(
            f"/api/v1/articles/{self.published_article.id}/editor/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "info")
        self.assertIn("redirect_url", response.data["data"])
        self.assertIn(
            self.published_article.slug, response.data["data"]["redirect_url"]
        )

    def test_published_author_gets_redirect(self):
        """Test that author gets redirect info for published article"""
        self.client.force_authenticate(user=self.author)
        response = self.client.get(
            f"/api/v1/articles/{self.published_article.id}/editor/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "info")
        self.assertIn("redirect_url", response.data["data"])
        self.assertIn(
            self.published_article.slug, response.data["data"]["redirect_url"]
        )

    def test_published_editor_gets_redirect(self):
        """Test that editor gets redirect info for published article"""
        self.client.force_authenticate(user=self.editor)
        response = self.client.get(
            f"/api/v1/articles/{self.published_article.id}/editor/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "info")
        self.assertIn("redirect_url", response.data["data"])
        self.assertIn(
            self.published_article.slug, response.data["data"]["redirect_url"]
        )

    def test_published_reviewer_gets_redirect(self):
        """Test that reviewer gets redirect info for published article"""
        self.client.force_authenticate(user=self.reviewer)
        response = self.client.get(
            f"/api/v1/articles/{self.published_article.id}/editor/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "info")
        self.assertIn("redirect_url", response.data["data"])
        self.assertIn(
            self.published_article.slug, response.data["data"]["redirect_url"]
        )

    def test_changes_requested_author_can_edit(self):
        """Test that author can edit article with changes requested"""
        self.review_article.status = ArticleStatusChoices.CHANGES_REQUESTED
        self.review_article.save()

        self.client.force_authenticate(user=self.author)
        response = self.client.get(f"/api/v1/articles/{self.review_article.id}/editor/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["user_can_edit"], True)


class UserBatchViewTestCase(APITestCase):
    """Test user batch lookup endpoint"""

    def setUp(self):

        self.user1 = TestUtil.verified_user()
        self.user2 = TestUtil.another_verified_user()

    def test_batch_requires_authentication(self):
        """Test that endpoint requires authentication"""
        response = self.client.post("/api/v1/users/batch/", {"user_ids": ["1"]})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_batch_requires_user_ids(self):
        """Test that userIds is required"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post("/api/v1/users/batch/", {})
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_batch_fetches_multiple_users(self):
        """Test fetching multiple users"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(
            "/api/v1/users/batch/",
            {"user_ids": [str(self.user1.id), str(self.user2.id)]},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 2)

    def test_batch_returns_user_info(self):
        """Test that response includes all user fields"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(
            "/api/v1/users/batch/", {"user_ids": [str(self.user1.id)]}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_data = response.data["data"][0]

        self.assertIn("id", user_data)
        self.assertIn("name", user_data)
        self.assertIn("avatar_url", user_data)
        self.assertIn("cursor_color", user_data)

    def test_batch_handles_nonexistent_users(self):
        """Test handling of non-existent user IDs"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(
            "/api/v1/users/batch/",
            {"user_ids": [str(self.user1.id), "123e4567-e89b-12d3-a456-426614174000"]},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only return existing user
        self.assertEqual(len(response.data["data"]), 1)


class UserSearchViewTestCase(APITestCase):
    """Test user search endpoint"""

    def setUp(self):

        self.author = TestUtil.verified_user()
        self.reviewer = TestUtil.another_verified_user()
        self.editor = TestUtil.other_verified_user()
        self.random_user = TestUtil.random_user()

        contributor_group, _ = Group.objects.get_or_create(name=UserRoles.CONTRIBUTOR)
        reviewer_group, _ = Group.objects.get_or_create(name=UserRoles.REVIEWER)
        editor_group, _ = Group.objects.get_or_create(name=UserRoles.EDITOR)

        self.author.groups.add(contributor_group)
        self.reviewer.groups.add(reviewer_group)
        self.editor.groups.add(editor_group)

        self.article = Article.objects.create(
            title="Test Article",
            content="Test content",
            author=self.author,
            status=ArticleStatusChoices.UNDER_REVIEW,
            assigned_reviewer=self.reviewer,
            assigned_editor=self.editor,
        )

    def test_search_requires_authentication(self):
        """Test that endpoint requires authentication"""
        response = self.client.get("/api/v1/users/search/?q=john&room_id=article-1")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_requires_query_param(self):
        """Test that query parameter is required"""
        self.client.force_authenticate(user=self.author)
        response = self.client.get("/api/v1/users/search/?room_id=article-1")
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_search_requires_room_id_param(self):
        """Test that room_id parameter is required"""
        self.client.force_authenticate(user=self.author)
        response = self.client.get("/api/v1/users/search/?q=john")
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_search_validates_room_id_format(self):
        """Test that room_id must start with 'article-'"""
        self.client.force_authenticate(user=self.author)
        response = self.client.get("/api/v1/users/search/?q=john&room_id=invalid-123")
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_search_filters_by_article_access(self):
        """Test that search only returns users with article access"""
        self.client.force_authenticate(user=self.author)
        response = self.client.get(
            f"/api/v1/users/search/?q=te&room_id=article-{self.article.id}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_ids = [user["id"] for user in response.data["data"]]

        # Should include author and reviewer
        self.assertIn(str(self.author.id), user_ids)
        self.assertIn(str(self.reviewer.id), user_ids)

        # Should NOT include random user
        self.assertNotIn(str(self.random_user.id), user_ids)

    def test_search_returns_empty_for_draft(self):
        """Test that draft articles return empty results"""
        self.article.status = ArticleStatusChoices.DRAFT
        self.article.save()

        self.client.force_authenticate(user=self.author)
        response = self.client.get(
            f"/api/v1/users/search/?q=john&room_id=article-{self.article.id}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 0)

    def test_search_includes_editor(self):
        """Test that editor is included when article"""
        self.article.status = ArticleStatusChoices.READY
        self.article.save()

        self.client.force_authenticate(user=self.author)
        response = self.client.get(
            f"/api/v1/users/search/?q=te&room_id=article-{self.article.id}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user_ids = [user["id"] for user in response.data["data"]]

        # Should include author, reviewer, and editor
        self.assertIn(str(self.author.id), user_ids)
        self.assertIn(str(self.reviewer.id), user_ids)
        self.assertIn(str(self.editor.id), user_ids)


# python manage.py test apps.content.tests.test_liveblocks.ArticleEditorViewTestCase
# python manage.py test apps.content.tests.test_liveblocks.UserBatchViewTestCase
# python manage.py test apps.content.tests.test_liveblocks.UserSearchViewTestCase
# python manage.py test apps.content.tests.test_liveblocks.LiveblocksAuthViewTests
# python manage.py test apps.content.tests.test_liveblocks.LiveblocksAuthViewTests
