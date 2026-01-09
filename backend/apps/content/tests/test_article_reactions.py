import uuid

from apps.common.errors import ErrorCode
from apps.common.utils import TestUtil
from apps.content.models import Article, ArticleReaction, ArticleStatusChoices, Category
from rest_framework import status
from rest_framework.test import APITestCase


class TestArticleReactions(APITestCase):

    def setUp(self):
        self.user1 = TestUtil.verified_user()
        self.user2 = TestUtil.other_verified_user()
        self.user3 = TestUtil.another_verified_user()

        self.category = Category.objects.create(
            name="Technology", desc="Technology related articles"
        )

        # Create published article
        self.published_article = Article.objects.create(
            title="Test Article",
            content="This is a test article content",
            author=self.user1,
            category=self.category,
            status=ArticleStatusChoices.PUBLISHED,
        )

        # Create draft article
        self.draft_article = Article.objects.create(
            title="Draft Article",
            content="This is a draft article",
            author=self.user1,
            category=self.category,
            status=ArticleStatusChoices.DRAFT,
        )

        self.pub_url = f"/api/v1/articles/{self.published_article.id}/reactions/"
        self.draft_url = f"/api/v1/articles/{self.draft_article.id}/reactions/"

    def test_toggle_reaction_unauthenticated(self):
        """Test 401 error when user is not authenticated"""
        data = {"reaction_type": "❤️"}
        response = self.client.post(self.pub_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_toggle_reaction_add_success(self):
        """Test successfully adding a reaction to an article"""
        self.client.force_authenticate(user=self.user2)

        data = {"reaction_type": "❤️"}
        response = self.client.post(self.pub_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()["data"]

        # Verify response structure
        self.assertEqual(response_data["reaction_type"], "❤️")
        self.assertEqual(response_data["action"], "added")
        self.assertTrue(response_data["is_reacted"])
        self.assertEqual(response_data["reaction_counts"]["❤️"], 1)
        self.assertEqual(response_data["total_reactions"], 1)

        self.assertTrue(
            ArticleReaction.objects.filter(
                article=self.published_article, user=self.user2, reaction_type="❤️"
            ).exists()
        )

    def test_toggle_reaction_remove_success(self):
        """Test successfully removing a reaction from an article"""
        ArticleReaction.objects.create(
            article=self.published_article, user=self.user2, reaction_type="❤️"
        )

        self.client.force_authenticate(user=self.user2)

        data = {"reaction_type": "❤️"}
        response = self.client.post(self.pub_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()["data"]

        # Verify response structure
        self.assertEqual(response_data["reaction_type"], "❤️")
        self.assertEqual(response_data["action"], "removed")
        self.assertFalse(response_data["is_reacted"])
        self.assertEqual(response_data["reaction_counts"].get("❤️", 0), 0)
        self.assertEqual(response_data["total_reactions"], 0)

        self.assertFalse(
            ArticleReaction.objects.filter(
                article=self.published_article, user=self.user2, reaction_type="❤️"
            ).exists()
        )

    def test_toggle_reaction_unpublished_article(self):
        """Test 403 error when trying to react to unpublished article"""
        self.client.force_authenticate(user=self.user2)

        data = {"reaction_type": "❤️"}
        response = self.client.post(self.draft_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()["code"], ErrorCode.FORBIDDEN)

    def test_toggle_reaction_multiple_reactions_same_user(self):
        """Test user can have multiple different reactions on same article"""
        self.client.force_authenticate(user=self.user2)

        # Add first reaction
        data1 = {"reaction_type": "❤️"}
        response1 = self.client.post(self.pub_url, data1)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        # Add second reaction
        data2 = {"reaction_type": "👍"}
        response2 = self.client.post(self.pub_url, data2)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        # Verify both reactions exist
        self.assertEqual(
            ArticleReaction.objects.filter(
                article=self.published_article, user=self.user2
            ).count(),
            2,
        )

        response_data = response2.json()["data"]
        self.assertEqual(response_data["total_reactions"], 2)
        self.assertEqual(response_data["reaction_counts"]["❤️"], 1)
        self.assertEqual(response_data["reaction_counts"]["👍"], 1)

    def test_toggle_reaction_article_not_found(self):
        """Test 404 error when article doesn't exist"""
        self.client.force_authenticate(user=self.user2)

        non_existent_id = uuid.uuid4()
        url = f"/api/v1/articles/{non_existent_id}/reactions/"
        data = {"reaction_type": "❤️"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_toggle_reaction_missing_reaction_type(self):
        """Test 422 error when reaction_type is missing"""
        self.client.force_authenticate(user=self.user2)

        response = self.client.post(self.pub_url, {})

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_toggle_reaction_invalid_reaction_type(self):
        """Test 422 error for invalid reaction type"""
        self.client.force_authenticate(user=self.user2)

        data = {"reaction_type": "invalid_emoji"}
        response = self.client.post(self.pub_url, data)

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_get_reaction_status_authenticated_with_reactions(self):
        """Test getting reaction status for authenticated user with reactions"""

        ArticleReaction.objects.create(
            article=self.published_article, user=self.user2, reaction_type="❤️"
        )
        ArticleReaction.objects.create(
            article=self.published_article, user=self.user2, reaction_type="👍"
        )
        ArticleReaction.objects.create(
            article=self.published_article, user=self.user3, reaction_type="❤️"
        )

        self.client.force_authenticate(user=self.user2)

        response = self.client.get(self.pub_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()["data"]

        # Verify response structure
        self.assertEqual(response_data["total_reactions"], 3)
        self.assertEqual(response_data["reaction_counts"]["❤️"], 2)
        self.assertEqual(response_data["reaction_counts"]["👍"], 1)
        self.assertIn("❤️", response_data["user_reactions"])
        self.assertIn("👍", response_data["user_reactions"])
        self.assertEqual(len(response_data["user_reactions"]), 2)

    def test_get_reaction_status_authenticated_without_reactions(self):
        """Test getting reaction status for authenticated user without reactions"""
        ArticleReaction.objects.create(
            article=self.published_article, user=self.user3, reaction_type="❤️"
        )

        self.client.force_authenticate(user=self.user2)

        response = self.client.get(self.pub_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()["data"]

        self.assertEqual(response_data["total_reactions"], 1)
        self.assertEqual(response_data["reaction_counts"]["❤️"], 1)
        self.assertEqual(response_data["user_reactions"], [])

    def test_get_reaction_status_unauthenticated(self):
        """Test getting reaction status for unauthenticated user"""
        ArticleReaction.objects.create(
            article=self.published_article, user=self.user2, reaction_type="❤️"
        )
        ArticleReaction.objects.create(
            article=self.published_article, user=self.user3, reaction_type="👍"
        )

        response = self.client.get(self.pub_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()["data"]

        self.assertEqual(response_data["total_reactions"], 2)
        self.assertEqual(response_data["reaction_counts"]["❤️"], 1)
        self.assertEqual(response_data["reaction_counts"]["👍"], 1)
        self.assertIsNone(response_data["user_reactions"])

    def test_get_reaction_status_article_not_found(self):
        """Test 404 error when getting status for non-existent article"""
        non_existent_id = uuid.uuid4()
        url = f"/api/v1/articles/{non_existent_id}/reactions/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_reaction_counts_aggregate_correctly(self):
        """Test that reaction counts aggregate correctly across users"""
        reactions = [
            (self.user1, "❤️"),
            (self.user2, "❤️"),
            (self.user3, "❤️"),
            (self.user1, "👍"),
            (self.user2, "😍"),
        ]

        for user, reaction in reactions:
            ArticleReaction.objects.create(
                article=self.published_article, user=user, reaction_type=reaction
            )

        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.pub_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()["data"]

        # Verify counts
        self.assertEqual(response_data["total_reactions"], 5)
        self.assertEqual(response_data["reaction_counts"]["❤️"], 3)
        self.assertEqual(response_data["reaction_counts"]["👍"], 1)
        self.assertEqual(response_data["reaction_counts"]["😍"], 1)

    def test_own_article_reaction_allowed(self):
        """Test that users can react to their own articles"""
        self.client.force_authenticate(user=self.user1)

        data = {"reaction_type": "❤️"}
        response = self.client.post(self.pub_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()["data"]
        self.assertEqual(response_data["action"], "added")


# python manage.py test apps.content.tests.test_article_reactions
