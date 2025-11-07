# from unittest.mock import patch
import uuid

from apps.accounts.models import ContributorOnboarding
from apps.accounts.utils import UserRoles
from apps.common.errors import ErrorCode
from apps.common.utils import TestUtil
from apps.content.models import (
    Article,
    ArticleReaction,
    ArticleStatusChoices,
    Category,
    Comment,
    CommentThread,
    Event,
    Job,
    Resource,
    Tag,
    Tool,
)
from django.contrib.auth.models import Group
from django.db.models import F
from rest_framework import status
from rest_framework.test import APITestCase

# import fakeredis


# TODO: FIX ISSUE WITH FAKE REDIS
# TODO: FIX SOME ERRORS OR WARNINGS IN THE TERMINAL E.G VALUEERROR


class TestContents(APITestCase):
    onboarding_url = "/api/v1/contribute/"
    articles_url = "/api/v1/articles/"
    tags_url = "/api/v1/tags/"
    jobs_url = "/api/v1/jobs/"
    events_url = "/api/v1/events/"
    resources_url = "/api/v1/resources/"
    tools_url = "/api/v1/tools/"
    create_comment_url = "/api/v1/comments/"

    def setUp(self):

        # # Mock Redis with fakeredis
        # self.fake_redis = fakeredis.FakeStrictRedis()
        # self.patcher = patch(
        #     'apps.content.services.redis.Redis',
        #     return_value=self.fake_redis
        # )
        # self.patcher.start()

        # from apps.content.services import CommentLikeService
        # from apps.content import services
        # services.comment_like_service = CommentLikeService()

        self.user1 = TestUtil.new_user()
        self.user2 = TestUtil.verified_user()
        self.user3 = TestUtil.other_verified_user()
        self.user4 = TestUtil.another_verified_user()
        self.contributor_group = Group.objects.get_or_create(name=UserRoles.CONTRIBUTOR)

        self.article = TestUtil.create_article(author=self.user4)
        self.comment = TestUtil.create_comment(article=self.article, user=self.user4)
        self.comment_del_url = f"/api/v1/comments/{self.comment.id}/"

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

        self.job1 = Job.objects.create(
            title="Software Engineer",
            company="Tech Co",
            location="San Francisco",
            category=self.category,
            salary=120000,
        )
        self.job2 = Job.objects.create(
            title="Data Scientist",
            company="Data Corp",
            location="New York",
            category=self.category,
            salary=150000,
        )

        self.event1 = Event.objects.create(
            title="Tech Conference",
            location="Las Vegas",
            category=self.category,
            start_date="2025-10-27",
            end_date="2025-10-29",
        )
        self.event2 = Event.objects.create(
            title="AI Summit",
            location="London",
            category=self.category,
            start_date="2025-11-05",
            end_date="2025-11-07",
        )

        self.resource1 = Resource.objects.create(
            name="Django Tutorial", category=self.category
        )
        self.resource2 = Resource.objects.create(
            name="React Docs", category=self.category
        )

        self.tool1 = Tool.objects.create(name="VS Code", category=self.category)
        self.tool2 = Tool.objects.create(name="PyCharm", category=self.category)

        self.root_comment = Comment.objects.create(
            article=self.published_article1,
            user=self.user2,
            body="This is a root comment",
        )
        self.thread = CommentThread.objects.create(
            article=self.published_article1,
            root_comment=self.root_comment,
        )
        self.root_comment.thread = self.thread
        self.root_comment.save()

        reply_data = [
            (self.user3, "First reply"),
            (self.user1, "Second reply"),
            (self.user2, "Third reply"),
        ]

        for user, body in reply_data:
            Comment.objects.create(
                article=self.published_article1,
                user=user,
                body=body,
                thread=self.thread,
            )
            CommentThread.objects.filter(id=self.thread.id).update(
                reply_count=F("reply_count") + 1
            )

        self.thread.refresh_from_db()

    # def tearDown(self):
    #     """Cleanup"""
    #     self.fake_redis.flushall()
    #     self.patcher.stop()
    #     super().tearDown()

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
        self.assertEqual(len(data["results"]), 3)

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

        self.assertIn("comments", data)

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

    def test_job_list(self):
        """Test job list endpoint"""
        response = self.client.get(self.jobs_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]

        self.assertEqual(len(data["results"]), 2)

    def test_event_list(self):
        """Test event list endpoint"""
        response = self.client.get(self.events_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]

        self.assertEqual(len(data["results"]), 2)

    def test_resource_list(self):
        """Test resource list endpoint"""
        response = self.client.get(self.resources_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]

        self.assertEqual(len(data["results"]), 2)

    def test_tool_list(self):
        """Test tool list endpoint"""
        response = self.client.get(self.tools_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]

        self.assertEqual(len(data["results"]), 2)

    def test_thread_replies_success_with_replies(self):
        url = f"/api/v1/comments/{self.root_comment.id}/replies/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]

        # Should return 3 replies (excluding root)
        self.assertEqual(len(data), 3)

        self.assertEqual(data[0]["body"], "First reply")
        self.assertEqual(data[1]["body"], "Second reply")
        self.assertEqual(data[2]["body"], "Third reply")

        # Verify root comment is NOT in replies
        reply_bodies = [reply["body"] for reply in data]
        self.assertNotIn("This is a root comment", reply_bodies)

        # Verify user information is included
        self.assertIn("user_name", data[0])
        self.assertIn("user_username", data[0])
        self.assertIn("user_avatar", data[0])
        self.assertEqual(data[0]["user_username"], self.user3.username)

    def test_thread_replies_empty_thread(self):
        root_comment = Comment.objects.create(
            article=self.published_article1,
            user=self.user2,
            body="Root comment with no replies",
        )
        thread = CommentThread.objects.create(
            article=self.published_article1,
            root_comment=root_comment,
        )
        root_comment.thread = thread
        root_comment.save()

        url = f"/api/v1/comments/{root_comment.id}/replies/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]
        self.assertEqual(len(data), 0)
        self.assertIsInstance(data, list)

    def test_thread_replies_excludes_inactive_replies(self):
        root_comment = Comment.objects.create(
            article=self.published_article1,
            user=self.user2,
            body="Root comment",
        )
        thread = CommentThread.objects.create(
            article=self.published_article1,
            root_comment=root_comment,
        )
        root_comment.thread = thread
        root_comment.save()

        # Create active and inactive replies
        Comment.objects.create(
            article=self.published_article1,
            user=self.user3,
            body="Active reply",
            thread=thread,
        )
        Comment.objects.create(
            article=self.published_article1,
            user=self.user1,
            body="Inactive reply (deleted)",
            thread=thread,
            is_active=False,  # Soft deleted
        )

        url = f"/api/v1/comments/{root_comment.id}/replies/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]

        # Should only return 1 active reply
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["body"], "Active reply")

        # Verify inactive reply is not included
        reply_bodies = [reply["body"] for reply in data]
        self.assertNotIn("Inactive reply (deleted)", reply_bodies)

    def test_thread_replies_comment_not_found(self):
        non_existent_id = uuid.uuid4()
        url = f"/api/v1/comments/{non_existent_id}/replies/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["message"], "Comment not found")
        self.assertEqual(response.json()["code"], ErrorCode.NON_EXISTENT)

    def test_thread_replies_inactive_root_comment(self):
        # Create inactive root comment
        inactive_root = Comment.objects.create(
            article=self.published_article1,
            user=self.user2,
            body="Deleted root comment",
            is_active=False,
        )

        url = f"/api/v1/comments/{inactive_root.id}/replies/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["message"], "Comment not found")
        self.assertEqual(response.json()["code"], ErrorCode.NON_EXISTENT)

    def test_thread_replies_for_reply_not_root(self):

        root_comment = Comment.objects.create(
            article=self.published_article1,
            user=self.user2,
            body="Root comment",
        )
        thread = CommentThread.objects.create(
            article=self.published_article1,
            root_comment=root_comment,
        )
        root_comment.thread = thread
        root_comment.save()

        # Create a reply (not a root)
        reply = Comment.objects.create(
            article=self.published_article1,
            user=self.user3,
            body="This is a reply",
            thread=thread,
        )

        # Try to fetch replies for the reply (should fail)
        url = f"/api/v1/comments/{reply.id}/replies/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_thread_replies_multiple_threads_no_contamination(self):
        """

        Ensure thread isolation.
        """

        root1 = Comment.objects.create(
            article=self.published_article1,
            user=self.user2,
            body="Root 1",
        )
        thread1 = CommentThread.objects.create(
            article=self.published_article1,
            root_comment=root1,
        )
        root1.thread = thread1
        root1.save()

        Comment.objects.create(
            article=self.published_article1,
            user=self.user3,
            body="Reply to thread 1",
            thread=thread1,
        )

        root2 = Comment.objects.create(
            article=self.published_article1,
            user=self.user1,
            body="Root 2",
        )
        thread2 = CommentThread.objects.create(
            article=self.published_article1,
            root_comment=root2,
        )
        root2.thread = thread2
        root2.save()

        Comment.objects.create(
            article=self.published_article1,
            user=self.user2,
            body="Reply to thread 2",
            thread=thread2,
        )

        # Fetch replies for thread 1
        url1 = f"/api/v1/comments/{root1.id}/replies/"
        response1 = self.client.get(url1)
        data1 = response1.json()["data"]

        # Should only contain thread 1 replies
        self.assertEqual(len(data1), 1)
        self.assertEqual(data1[0]["body"], "Reply to thread 1")

        # Fetch replies for thread 2
        url2 = f"/api/v1/comments/{root2.id}/replies/"
        response2 = self.client.get(url2)
        data2 = response2.json()["data"]

        # Should only contain thread 2 replies
        self.assertEqual(len(data2), 1)
        self.assertEqual(data2[0]["body"], "Reply to thread 2")

    def test_thread_replies_max_replies(self):
        """
        Test thread with maximum replies (100).
        Ensure all replies are returned and properly ordered.
        """

        root_comment = Comment.objects.create(
            article=self.published_article1,
            user=self.user2,
            body="Root with many replies",
        )
        thread = CommentThread.objects.create(
            article=self.published_article1,
            root_comment=root_comment,
        )
        root_comment.thread = thread
        root_comment.save()

        # Create 100 replies
        replies = []
        for i in range(100):
            reply = Comment.objects.create(
                article=self.published_article1,
                user=self.user3 if i % 2 == 0 else self.user1,
                body=f"Reply number {i+1}",
                thread=thread,
            )
            replies.append(reply)

        url = f"/api/v1/comments/{root_comment.id}/replies/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]

        # Should return all 100 replies
        self.assertEqual(len(data), 100)

        # Verify chronological order
        self.assertEqual(data[0]["body"], "Reply number 1")
        self.assertEqual(data[99]["body"], "Reply number 100")

    def test_comment_create_unauthenticated(self):
        data = {
            "article_id": str(self.published_article1.id),
            "body": "This should fail",
        }

        response = self.client.post(self.create_comment_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_create_root_comment_success(self):
        self.client.force_authenticate(user=self.user1)

        data = {
            "article_id": str(self.published_article1.id),
            "body": "This is a new root comment",
        }

        response = self.client.post(self.create_comment_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()["data"]

        # Verify response structure
        self.assertIn("id", response_data)
        self.assertIn("thread_id", response_data)
        self.assertEqual(response_data["body"], "This is a new root comment")
        self.assertEqual(response_data["user_username"], self.user1.username)
        self.assertEqual(response_data["user_name"], self.user1.full_name)
        self.assertTrue(response_data["is_root"])

        # Verify database state
        comment = Comment.objects.get(id=response_data["id"])
        self.assertEqual(comment.article, self.published_article1)
        self.assertEqual(comment.user, self.user1)
        self.assertIsNotNone(comment.thread)
        self.assertEqual(comment.thread.root_comment, comment)
        self.assertEqual(comment.thread.reply_count, 0)
        self.assertTrue(comment.is_root_comment)

    def test_comment_create_reply_success(self):

        self.client.force_authenticate(user=self.user1)

        data = {
            "article_id": str(self.published_article1.id),
            "thread_id": str(self.thread.id),
            "body": "This is a reply to the thread",
        }

        # Get initial reply count
        initial_reply_count = self.thread.reply_count

        response = self.client.post(self.create_comment_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()["data"]

        # Verify response structure
        self.assertEqual(response_data["body"], "This is a reply to the thread")
        self.assertEqual(response_data["user_username"], self.user1.username)
        self.assertEqual(response_data["thread_id"], str(self.thread.id))
        self.assertFalse(response_data["is_root"])

        # Verify database state
        comment = Comment.objects.get(id=response_data["id"])
        self.assertEqual(comment.thread, self.thread)
        self.assertFalse(comment.is_root_comment)

        # Verify thread reply count incremented
        self.thread.refresh_from_db()
        self.assertEqual(self.thread.reply_count, initial_reply_count + 1)

    def test_comment_create_missing_article_id(self):
        self.client.force_authenticate(user=self.user1)

        data = {
            "body": "Comment without article_id",
        }

        response = self.client.post(self.create_comment_url, data)

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_comment_create_missing_body(self):
        self.client.force_authenticate(user=self.user1)

        data = {
            "article_id": str(self.published_article1.id),
        }

        response = self.client.post(self.create_comment_url, data)

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_comment_create_article_not_found(self):

        self.client.force_authenticate(user=self.user1)

        non_existent_id = uuid.uuid4()
        data = {
            "article_id": str(non_existent_id),
            "body": "Comment on non-existent article",
        }

        response = self.client.post(self.create_comment_url, data)

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data["code"], ErrorCode.VALIDATION_ERROR)

    def test_comment_create_unpublished_article(self):

        self.client.force_authenticate(user=self.user1)

        data = {
            "article_id": str(self.draft_article.id),
            "body": "Comment on draft article",
        }

        response = self.client.post(self.create_comment_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["code"], ErrorCode.FORBIDDEN)

    def test_comment_create_thread_not_found(self):

        self.client.force_authenticate(user=self.user1)

        non_existent_thread_id = uuid.uuid4()
        data = {
            "article_id": str(self.published_article1.id),
            "thread_id": str(non_existent_thread_id),
            "body": "Reply to non-existent thread",
        }

        response = self.client.post(self.create_comment_url, data)

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data["code"], ErrorCode.VALIDATION_ERROR)

    def test_comment_create_thread_article_mismatch(self):
        # Create a thread on different article
        other_root = Comment.objects.create(
            article=self.published_article2,
            user=self.user2,
            body="Root on different article",
        )
        other_thread = CommentThread.objects.create(
            article=self.published_article2,
            root_comment=other_root,
        )
        other_root.thread = other_thread
        other_root.save()

        self.client.force_authenticate(user=self.user1)

        data = {
            "article_id": str(self.published_article1.id),
            "thread_id": str(other_thread.id),
            "body": "Reply to wrong article's thread",
        }

        response = self.client.post(self.create_comment_url, data)

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data["code"], ErrorCode.VALIDATION_ERROR)

    def test_comment_create_thread_max_replies_reached(self):
        # Create a thread with 100 replies
        root_comment = Comment.objects.create(
            article=self.published_article1,
            user=self.user2,
            body="Root with max replies",
        )
        thread = CommentThread.objects.create(
            article=self.published_article1,
            root_comment=root_comment,
            reply_count=100,
        )
        root_comment.thread = thread
        root_comment.save()

        self.client.force_authenticate(user=self.user1)

        data = {
            "article_id": str(self.published_article1.id),
            "thread_id": str(thread.id),
            "body": "This should fail - thread full",
        }

        response = self.client.post(self.create_comment_url, data)

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.data["code"], ErrorCode.VALIDATION_ERROR)

    def test_comment_create_inactive_thread(self):
        # Create inactive thread
        inactive_root = Comment.objects.create(
            article=self.published_article1,
            user=self.user2,
            body="Inactive thread root",
        )
        inactive_thread = CommentThread.objects.create(
            article=self.published_article1,
            root_comment=inactive_root,
            is_active=False,
        )
        inactive_root.thread = inactive_thread
        inactive_root.save()

        self.client.force_authenticate(user=self.user1)

        data = {
            "article_id": str(self.published_article1.id),
            "thread_id": str(inactive_thread.id),
            "body": "Reply to inactive thread",
        }

        response = self.client.post(self.create_comment_url, data)

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_comment_create_empty_body(self):
        """Test 422 error when body is empty string"""
        self.client.force_authenticate(user=self.user1)

        data = {
            "article_id": str(self.published_article1.id),
            "body": "",
        }

        response = self.client.post(self.create_comment_url, data)

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_comment_create_multiple_replies_same_thread(self):

        self.client.force_authenticate(user=self.user1)

        # First reply
        data1 = {
            "article_id": str(self.published_article1.id),
            "thread_id": str(self.thread.id),
            "body": "First reply from user1",
        }
        response1 = self.client.post(self.create_comment_url, data1)

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Second reply
        data2 = {
            "article_id": str(self.published_article1.id),
            "thread_id": str(self.thread.id),
            "body": "Second reply from user1",
        }
        response2 = self.client.post(self.create_comment_url, data2)

        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        # Verify thread reply count
        self.thread.refresh_from_db()
        # Initial setup had 3 replies + 2 new = 5
        self.assertEqual(self.thread.reply_count, 5)

    def test_delete_comment_unauthenticated(self):
        response = self.client.delete(self.comment_del_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_comment_not_author(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(self.comment_del_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())

    def test_delete_comment_success(self):
        self.client.force_authenticate(user=self.user4)
        response = self.client.delete(self.comment_del_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

    def test_delete_non_existent_comment(self):
        non_existent_uuid = "12345678-1234-5678-1234-567812345678"
        url = f"/api/v1/comments/{non_existent_uuid}/"
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_like_toggle_unauthenticated(self):
        """Test 401 error when user is not authenticated"""
        url = f"/api/v1/comments/{self.comment.id}/like/"
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_like_toggle_add_success(self):
        """Test successfully liking a comment"""
        self.client.force_authenticate(user=self.user2)
        url = f"/api/v1/comments/{self.comment.id}/like/"

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()["data"]

        # Verify response structure
        self.assertEqual(str(response_data["comment_id"]), str(self.comment.id))
        self.assertTrue(response_data["is_liked"])
        self.assertEqual(response_data["like_count"], 1)

    def test_comment_like_toggle_remove_success(self):
        """Test successfully unliking a comment"""
        self.client.force_authenticate(user=self.user2)
        url = f"/api/v1/comments/{self.comment.id}/like/"

        # First like the comment
        self.client.post(url)

        # Then unlike it
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()["data"]

        # Verify response structure
        self.assertEqual(str(response_data["comment_id"]), str(self.comment.id))
        self.assertFalse(response_data["is_liked"])
        self.assertEqual(response_data["like_count"], 0)

    def test_comment_like_toggle_multiple_users(self):
        """Test multiple users can like the same comment"""
        url = f"/api/v1/comments/{self.comment.id}/like/"

        # User2 likes
        self.client.force_authenticate(user=self.user2)
        response1 = self.client.post(url)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        # User3 likes
        self.client.force_authenticate(user=self.user3)
        response2 = self.client.post(url)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        response_data = response2.json()["data"]
        self.assertEqual(response_data["like_count"], 2)

    def test_comment_like_toggle_comment_not_found(self):
        """Test 404 error when comment doesn't exist"""
        self.client.force_authenticate(user=self.user2)

        non_existent_id = uuid.uuid4()
        url = f"/api/v1/comments/{non_existent_id}/like/"

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_like_toggle_inactive_comment(self):
        """Test 404 error when trying to like inactive/deleted comment"""
        # Create inactive comment
        inactive_comment = Comment.objects.create(
            article=self.article,
            user=self.user4,
            body="Inactive comment",
            is_active=False,
        )

        self.client.force_authenticate(user=self.user2)
        url = f"/api/v1/comments/{inactive_comment.id}/like/"

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_like_status_authenticated_with_like(self):
        """Test getting like status for authenticated user who liked"""
        self.client.force_authenticate(user=self.user2)

        # Like the comment first
        like_url = f"/api/v1/comments/{self.comment.id}/like/"
        self.client.post(like_url)

        # Get status
        status_url = f"/api/v1/comments/{self.comment.id}/likes/"
        response = self.client.get(status_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()["data"]

        # Verify response structure
        self.assertEqual(str(response_data["comment_id"]), str(self.comment.id))
        self.assertTrue(response_data["is_liked"])
        self.assertEqual(response_data["like_count"], 1)

    def test_comment_like_status_authenticated_without_like(self):
        """Test getting like status for authenticated user who hasn't liked"""
        # Another user likes the comment
        self.client.force_authenticate(user=self.user3)
        like_url = f"/api/v1/comments/{self.comment.id}/like/"
        self.client.post(like_url)

        # User2 checks status (hasn't liked)
        self.client.force_authenticate(user=self.user2)
        status_url = f"/api/v1/comments/{self.comment.id}/likes/"
        response = self.client.get(status_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()["data"]

        # Verify response structure
        self.assertEqual(str(response_data["comment_id"]), str(self.comment.id))
        self.assertFalse(response_data["is_liked"])
        self.assertEqual(response_data["like_count"], 1)

    def test_comment_like_status_unauthenticated(self):
        """Test getting like status for unauthenticated user"""
        # User2 likes the comment
        self.client.force_authenticate(user=self.user2)
        like_url = f"/api/v1/comments/{self.comment.id}/like/"
        self.client.post(like_url)

        # Guest checks status
        self.client.force_authenticate(user=None)
        status_url = f"/api/v1/comments/{self.comment.id}/likes/"
        response = self.client.get(status_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()["data"]

        # Verify response structure
        self.assertEqual(str(response_data["comment_id"]), str(self.comment.id))
        self.assertIsNone(response_data["is_liked"])
        self.assertEqual(response_data["like_count"], 1)

    def test_comment_like_status_multiple_likes(self):
        """Test like count with multiple users"""
        like_url = f"/api/v1/comments/{self.comment.id}/like/"

        # Multiple users like
        for user in [self.user1, self.user2, self.user3]:
            self.client.force_authenticate(user=user)
            self.client.post(like_url)

        # Check status
        status_url = f"/api/v1/comments/{self.comment.id}/likes/"
        response = self.client.get(status_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()["data"]

        self.assertEqual(response_data["like_count"], 3)
        self.assertTrue(response_data["is_liked"])  # user3 is still authenticated

    def test_comment_like_status_comment_not_found(self):
        """Test 404 error when getting status for non-existent comment"""
        self.client.force_authenticate(user=self.user2)

        non_existent_id = uuid.uuid4()
        url = f"/api/v1/comments/{non_existent_id}/likes/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_like_status_inactive_comment(self):
        """Test 404 error when getting status for inactive comment"""
        # Create inactive comment
        inactive_comment = Comment.objects.create(
            article=self.article,
            user=self.user4,
            body="Inactive comment",
            is_active=False,
        )

        self.client.force_authenticate(user=self.user2)
        url = f"/api/v1/comments/{inactive_comment.id}/likes/"

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_like_status_no_likes(self):
        """Test getting status for comment with no likes"""
        self.client.force_authenticate(user=self.user2)

        status_url = f"/api/v1/comments/{self.comment.id}/likes/"
        response = self.client.get(status_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()["data"]

        self.assertEqual(response_data["like_count"], 0)
        self.assertFalse(response_data["is_liked"])


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


# python manage.py test apps.content.tests.TestContents -k thread_replies
# python manage.py test apps.content.tests.TestContents.test_comment_like_toggle_unauthenticated
# python manage.py test apps.content.tests.TestArticleReactions.test_toggle_reaction_unauthenticated
# python manage.py test apps.content.tests.TestArticleReactions.test_toggle_reaction_unauthenticated
