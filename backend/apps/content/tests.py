from apps.accounts.models import ContributorOnboarding
from apps.accounts.utils import UserRoles
from apps.common.utils import TestUtil
from apps.content.models import Article, ArticleStatusChoices, Category, Tag
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase


class TestContents(APITestCase):
    onboarding_url = "/api/v1/contribute/"
    articles_url = "/api/v1/articles/"
    tags_url = "/api/v1/tags/"

    def setUp(self):
        self.user1 = TestUtil.new_user()
        self.user2 = TestUtil.verified_user()
        self.user3 = TestUtil.other_verified_user()
        self.contributor_group = Group.objects.get_or_create(name=UserRoles.CONTRIBUTOR)

        # Create test data
        self.category = Category.objects.create(
            name="Technology", desc="Technology related articles"
        )

        self.tag1 = Tag.objects.create(name="python")
        self.tag2 = Tag.objects.create(name="django")
        self.tag3 = Tag.objects.create(name="testing")

        # Create published articles
        self.published_article1 = Article.objects.create(
            title="Published Article 1",
            content="This is a published article content",
            author=self.user2,
            category=self.category,
            status=ArticleStatusChoices.PUBLISHED,
        )
        self.published_article1.tags.set([self.tag1, self.tag2])

        self.published_article2 = Article.objects.create(
            title="Published Article 2",
            content="Another published article content",
            author=self.user3,
            category=self.category,
            status=ArticleStatusChoices.PUBLISHED,
        )
        self.published_article2.tags.set([self.tag2, self.tag3])

        # Create draft article (should not appear in public list)
        self.draft_article = Article.objects.create(
            title="Draft Article",
            content="This is a draft article",
            author=self.user2,
            category=self.category,
            status=ArticleStatusChoices.DRAFT,
        )

    def test_onboarding(self):
        self.valid_data = {"terms_accepted": True}
        self.invalid_data = {"terms_accepted": False}
        # invalid_data_sets = [
        #     {"terms_accepted": "true"},
        #     {"terms_accepted": 1},
        #     {"terms_accepted": None},
        # ]

        # 401
        response = self.client.post(self.onboarding_url, self.valid_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # 422 - Validation error
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(self.onboarding_url, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertFalse(self.user1.groups.filter(name=UserRoles.CONTRIBUTOR).exists())
        self.assertFalse(ContributorOnboarding.objects.filter(user=self.user1).exists())

        # 422
        # for invalid_data in invalid_data_sets:
        #     with self.subTest(data=invalid_data):
        #         response = self.client.post(self.onboarding_url, invalid_data)
        #         print(response.json())
        #         self.assertEqual(
        #             response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY
        #         )

        # 422
        response = self.client.post(self.onboarding_url, {})
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertFalse(self.user1.groups.filter(name=UserRoles.CONTRIBUTOR).exists())

        # 200 - Already contributor
        contributor_group = Group.objects.get(name=UserRoles.CONTRIBUTOR)
        self.user1.groups.add(contributor_group)
        response = self.client.post(self.onboarding_url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 201 - Successfully became contributor
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(self.onboarding_url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.user2.refresh_from_db()
        self.assertTrue(self.user2.groups.filter(name=UserRoles.CONTRIBUTOR).exists())

        self.assertTrue(ContributorOnboarding.objects.filter(user=self.user2).exists())

        onboarding_record = ContributorOnboarding.objects.get(user=self.user2)
        self.assertTrue(onboarding_record.terms_accepted)
        self.assertIsNotNone(onboarding_record.accepted_at)

    def test_article_list(self):
        """Test article list endpoint returns only published articles"""
        response = self.client.get(self.articles_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.json())

        # Should return 2 published articles
        data = response.json()["data"]
        self.assertEqual(len(data["results"]), 2)

        # Verify only published articles are returned
        article_titles = [article["title"] for article in data["results"]]
        self.assertIn("Published Article 1", article_titles)
        self.assertIn("Published Article 2", article_titles)
        self.assertNotIn("Draft Article", article_titles)

    def test_article_detail(self):
        """Test article detail endpoint returns published article details"""
        # Test successful retrieval of published article
        article_detail_url = (
            f"/api/v1/articles/{self.user2.username}/{self.published_article1.slug}/"
        )
        response = self.client.get(article_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.json())

        data = response.json()["data"]

        self.assertEqual(data["title"], "Published Article 1")
        self.assertEqual(data["content"], "This is a published article content")
        self.assertEqual(data["author"], self.user2.full_name)
        self.assertEqual(data["status"], ArticleStatusChoices.PUBLISHED)

        # Test 404 for non-existent article
        non_existent_url = f"/api/v1/articles/{self.user2.username}/non-existent-slug/"
        not_found_response = self.client.get(non_existent_url)
        self.assertEqual(not_found_response.status_code, status.HTTP_404_NOT_FOUND)

        # Test 404 for draft article (not published)
        draft_url = f"/api/v1/articles/{self.user2.username}/{self.draft_article.slug}/"
        draft_response = self.client.get(draft_url)
        self.assertEqual(draft_response.status_code, status.HTTP_404_NOT_FOUND)

        # Test 404 for non-existent user
        invalid_user_url = (
            f"/api/v1/articles/nonexistentuser/{self.published_article1.slug}/"
        )
        invalid_user_response = self.client.get(invalid_user_url)
        self.assertEqual(invalid_user_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_tag_list(self):
        """Test tag list endpoint returns all tags"""

        response = self.client.get(self.tags_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.json())

        data = response.json()["data"]
        self.assertEqual(len(data), 3)  # We created 3 tags

        # Verify tag names are returned (should be lowercase due to Tag.clean())
        tag_names = [tag["name"] for tag in data]
        self.assertIn("python", tag_names)
        self.assertIn("django", tag_names)
        self.assertIn("testing", tag_names)

        # Test limit parameter
        limit_response = self.client.get(f"{self.tags_url}?limit=2")
        self.assertEqual(limit_response.status_code, status.HTTP_200_OK)
        limit_data = limit_response.json()["data"]
        self.assertEqual(len(limit_data), 2)

        # Test invalid limit parameter (should use default)
        invalid_limit_response = self.client.get(f"{self.tags_url}?limit=invalid")
        self.assertEqual(invalid_limit_response.status_code, status.HTTP_200_OK)
        invalid_limit_data = invalid_limit_response.json()["data"]
        self.assertEqual(
            len(invalid_limit_data), 3
        )  # Should return all tags since we have only 3


# python manage.py test apps.content.tests.TestContents.test_article_list
