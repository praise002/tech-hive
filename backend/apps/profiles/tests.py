from apps.accounts.models import User
from apps.accounts.utils import UserRoles
from apps.common.utils import TestUtil
from apps.content.models import Article, ArticleStatusChoices
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase


class TestProfiles(APITestCase):
    profile_url = "/api/v1/profiles/me/"
    profile_detail_url = "/api/v1/profiles/<str:username>/"
    avatar_update_url = "/api/v1/profiles/avatar/"
    article_list_url = "/api/v1/profiles/me/articles/"
    article_detail_url = "/api/v1/profiles/me/articles/<slug:slug>/"

    def setUp(self):
        self.user1 = TestUtil.verified_user()
        self.user2 = TestUtil.other_verified_user()
        self.contributor_group = Group.objects.get_or_create(name=UserRoles.CONTRIBUTOR)

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

    def test_user_article_get(self):
        contributor_group = Group.objects.get(name=UserRoles.CONTRIBUTOR)
        self.user1.groups.add(contributor_group)
        self.user2.groups.add(contributor_group)

        Article.objects.create(
            title="Test Article 1",
            content="Test content 1",
            author=self.user1,
            status=ArticleStatusChoices.DRAFT,
        )
        Article.objects.create(
            title="Test Article 2",
            content="Test content 2",
            author=self.user1,
            status=ArticleStatusChoices.PUBLISHED,
        )

        # Create article for user2 (should not appear in user1's list)
        Article.objects.create(
            title="User2 Article",
            content="User2 content",
            author=self.user2,
            status=ArticleStatusChoices.DRAFT,
        )

        # Test: Contributor can get their own articles - 200
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.article_list_url)
        self.assertEqual(response.status_code, 200)

        # Should only return user1's articles
        articles = response.data["data"]["results"]
        self.assertEqual(len(articles), 2)
        article_titles = [article["title"] for article in articles]
        self.assertIn("Test Article 1", article_titles)
        self.assertIn("Test Article 2", article_titles)

        # Test: 401 for unauthenticated users
        self.client.force_authenticate(user=None)
        response = self.client.get(self.article_list_url)
        self.assertEqual(response.status_code, 401)

        # Test: 403 for non-contributor users
        self.user1.groups.remove(contributor_group)

        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.article_list_url)
        self.assertEqual(response.status_code, 403)

    def test_user_article_post(self):
        # Test: Contributor can create articles - 201
        self.client.force_authenticate(user=self.user1)
        contributor_group = Group.objects.get(name=UserRoles.CONTRIBUTOR)
        self.user1.groups.add(contributor_group)

        article_data = {
            "title": "New Test Article",
            "content": "This is test content for the new article",
        }

        response = self.client.post(self.article_list_url, article_data)
        self.assertEqual(response.status_code, 201)

        # Verify article was created
        created_article = Article.objects.get(title="New Test Article")
        self.assertEqual(created_article.author, self.user1)
        self.assertEqual(created_article.status, ArticleStatusChoices.DRAFT)

        # Test: 401 for unauthenticated users
        self.client.force_authenticate(user=None)
        response = self.client.post(self.article_list_url, article_data, format="json")
        self.assertEqual(response.status_code, 401)

        # Test: 403 for non-contributor users
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(self.article_list_url, article_data, format="json")
        self.assertEqual(response.status_code, 403)

    def test_article_retrieve(self):
        # Create test articles with different statuses
        draft_article = Article.objects.create(
            title="Draft Article",
            content="Draft content",
            author=self.user1,
            status=ArticleStatusChoices.DRAFT,
            slug="draft-article",
        )

        published_article = Article.objects.create(
            title="Published Article",
            content="Published content",
            author=self.user1,
            status=ArticleStatusChoices.PUBLISHED,
            slug="published-article",
        )

        rejected_article = Article.objects.create(
            title="Rejected Article",
            content="Rejected content",
            author=self.user1,
            status=ArticleStatusChoices.REJECTED,
            slug="rejected-article",
        )

        changes_requested_article = Article.objects.create(
            title="Changes Requested Article",
            content="Changes Requested content",
            author=self.user1,
            status=ArticleStatusChoices.CHANGES_REQUESTED,
            slug="changes-requested-article",
        )

        submitted_for_review_article = Article.objects.create(
            title="Submitted for Review Article",
            content="Submitted for Review content",
            author=self.user1,
            status=ArticleStatusChoices.SUBMITTED_FOR_REVIEW,
            slug="submitted-for-review-article",
        )

        under_review_article = Article.objects.create(
            title="Under Review Article",
            content="Under Review content",
            author=self.user1,
            status=ArticleStatusChoices.UNDER_REVIEW,
            slug="under-review-article",
        )

        review_completed_article = Article.objects.create(
            title="Review Completed Article",
            content="Review Completed content",
            author=self.user1,
            status=ArticleStatusChoices.REVIEW_COMPLETED,
            slug="review-completed-article",
        )

        ready_article = Article.objects.create(
            title="Ready Article",
            content="Ready content",
            author=self.user1,
            status=ArticleStatusChoices.READY,
            slug="ready-article",
        )

        # Test: Can retrieve non-published articles as contributor - 200
        contributor_group = Group.objects.get(name=UserRoles.CONTRIBUTOR)
        self.user1.groups.add(contributor_group)
        self.client.force_authenticate(user=self.user1)

        # Should be able to retrieve draft article
        response = self.client.get(
            self.article_detail_url.replace("<slug:slug>", draft_article.slug)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["title"], "Draft Article")

        # Should be able to retrieve rejected article
        response = self.client.get(
            self.article_detail_url.replace("<slug:slug>", rejected_article.slug)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["title"], "Rejected Article")

        # Should be able to retrieve under review article
        response = self.client.get(
            self.article_detail_url.replace("<slug:slug>", under_review_article.slug)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["title"], "Under Review Article")

        # Should be able to retrieve changes requested article
        response = self.client.get(
            self.article_detail_url.replace(
                "<slug:slug>", changes_requested_article.slug
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["title"], "Changes Requested Article")

        # Should be able to retrieve review completed article
        response = self.client.get(
            self.article_detail_url.replace(
                "<slug:slug>", review_completed_article.slug
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["title"], "Review Completed Article")

        # Should be able to retrieve ready article
        response = self.client.get(
            self.article_detail_url.replace("<slug:slug>", ready_article.slug)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["title"], "Ready Article")

        # Should be able to retrieve submitted for review article
        response = self.client.get(
            self.article_detail_url.replace(
                "<slug:slug>", submitted_for_review_article.slug
            )
        )
        self.assertEqual(response.status_code, 200)

        # Should NOT be able to retrieve published article (excluded from view)
        response = self.client.get(
            self.article_detail_url.replace("<slug:slug>", published_article.slug)
        )
        self.assertEqual(response.status_code, 404)

        # Test: 401 for unauthenticated users
        self.client.force_authenticate(user=None)
        response = self.client.get(
            self.article_detail_url.replace("<slug:slug>", draft_article.slug)
        )
        self.assertEqual(response.status_code, 401)

        # Test: 403 for user trying to retrieve another user's article
        self.user2.groups.add(contributor_group)
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(
            self.article_detail_url.replace("<slug:slug>", draft_article.slug),
        )
        self.assertEqual(response.status_code, 403)

        # Test: 404 for non-existent article
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(
            self.article_detail_url.replace("<slug:slug>", "non-existent-slug")
        )
        self.assertEqual(response.status_code, 404)

    def test_article_update(self):
        # Create test articles with different statuses
        draft_article = Article.objects.create(
            title="Draft Article",
            content="Draft content",
            author=self.user1,
            status=ArticleStatusChoices.DRAFT,
            slug="draft-article",
        )

        published_article = Article.objects.create(
            title="Published Article",
            content="Published content",
            author=self.user1,
            status=ArticleStatusChoices.PUBLISHED,
            slug="published-article",
        )

        rejected_article = Article.objects.create(
            title="Rejected Article",
            content="Rejected content",
            author=self.user1,
            status=ArticleStatusChoices.REJECTED,
            slug="rejected-article",
        )

        changes_requested_article = Article.objects.create(
            title="Changes Requested Article",
            content="Changes Requested content",
            author=self.user1,
            status=ArticleStatusChoices.CHANGES_REQUESTED,
            slug="changes-requested-article",
        )

        submitted_for_review_article = Article.objects.create(
            title="Submitted for Review Article",
            content="Submitted for Review content",
            author=self.user1,
            status=ArticleStatusChoices.SUBMITTED_FOR_REVIEW,
            slug="submitted-for-review-article",
        )

        under_review_article = Article.objects.create(
            title="Under Review Article",
            content="Under Review content",
            author=self.user1,
            status=ArticleStatusChoices.UNDER_REVIEW,
            slug="under-review-article",
        )

        review_completed_article = Article.objects.create(
            title="Review Completed Article",
            content="Review Completed content",
            author=self.user1,
            status=ArticleStatusChoices.REVIEW_COMPLETED,
            slug="review-completed-article",
        )

        ready_article = Article.objects.create(
            title="Ready Article",
            content="Ready content",
            author=self.user1,
            status=ArticleStatusChoices.READY,
            slug="ready-article",
        )

        # Test: 200 - Can update editable articles
        self.client.force_authenticate(user=self.user1)
        contributor_group = Group.objects.get(name=UserRoles.CONTRIBUTOR)
        self.user1.groups.add(contributor_group)

        update_data = {"title": "Updated Draft Article"}

        # Should be able to update draft article
        response = self.client.patch(
            self.article_detail_url.replace("<slug:slug>", draft_article.slug),
            update_data,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["title"], "Updated Draft Article")

        # Should be able to update changes requested article
        response = self.client.patch(
            self.article_detail_url.replace(
                "<slug:slug>", changes_requested_article.slug
            ),
            {"title": "Updated Changes Requested Article"},
        )
        self.assertEqual(response.status_code, 200)

        # Should be able to update rejected article
        response = self.client.patch(
            self.article_detail_url.replace("<slug:slug>", rejected_article.slug),
            {"title": "Updated Rejected Article"},
        )
        self.assertEqual(response.status_code, 200)

        # Should NOT be able to update published article (permission denied)
        response = self.client.patch(
            self.article_detail_url.replace("<slug:slug>", published_article.slug),
            update_data,
        )
        self.assertEqual(response.status_code, 403)

        # Should NOT be able to update submitted for review article (permission denied)
        response = self.client.patch(
            self.article_detail_url.replace(
                "<slug:slug>", submitted_for_review_article.slug
            ),
            update_data,
        )
        self.assertEqual(response.status_code, 403)

        # Should NOT be able to update under review article (permission denied)
        response = self.client.patch(
            self.article_detail_url.replace("<slug:slug>", under_review_article.slug),
            update_data,
        )
        self.assertEqual(response.status_code, 403)

        # Should NOT be able to update review completed article (permission denied)
        response = self.client.patch(
            self.article_detail_url.replace(
                "<slug:slug>", review_completed_article.slug
            ),
            update_data,
        )
        self.assertEqual(response.status_code, 403)

        # Should NOT be able to update ready article (permission denied)
        response = self.client.patch(
            self.article_detail_url.replace("<slug:slug>", ready_article.slug),
            update_data,
        )
        self.assertEqual(response.status_code, 403)

        # Test: 401 for unauthenticated users
        self.client.force_authenticate(user=None)
        response = self.client.patch(
            self.article_detail_url.replace("<slug:slug>", draft_article.slug),
            update_data,
        )
        self.assertEqual(response.status_code, 401)

        # Test: 403 for user trying to update another user's article
        # print(contributor_group)
        # self.user2.groups.add(contributor_group)
        # self.client.force_authenticate(user=self.user2)
        # # response = self.client.patch(
        # #     self.article_detail_url.replace("<slug:slug>", draft_article.slug),
        # #     update_data,
        # # )
        # # print(response.data)
        # # self.assertEqual(response.status_code, 403)
        # print(f"User1: {self.user1.id}, User2: {self.user2.id}")  # DEBUG
        # print(f"Article author: {draft_article.author.id}")  # DEBUG
        # print(f"Article slug: {draft_article.slug}")  # DEBUG

        # url = self.article_detail_url.replace("<slug:slug>", draft_article.slug)

        # print(f"Request URL: {url}")  # DEBUG

        # response = self.client.patch(url, update_data)
        # print(f"Response status: {response.status_code}")  # DEBUG
        # print(f"Response data: {response.data}")  # DEBUG


# python manage.py test apps.profiles.tests.TestProfiles
