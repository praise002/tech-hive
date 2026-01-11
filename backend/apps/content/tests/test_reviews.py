import uuid

from apps.accounts.utils import UserRoles
from apps.common.utils import TestUtil
from apps.content.choices import ArticleReviewStatusChoices, ArticleStatusChoices
from apps.content.models import Article, ArticleReview
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AssignedReviewsListViewTests(APITestCase):
    """
    Test suite for AssignedReviewsListView endpoint.
    Tests authentication, permissions, filtering, and response format.
    """

    def setUp(self):
        """Set up test users, articles, and reviews"""

        self.reviewer_group = Group.objects.get_or_create(name=UserRoles.REVIEWER)[0]
        self.contributor_group = Group.objects.get_or_create(
            name=UserRoles.CONTRIBUTOR
        )[0]

        self.reviewer1 = TestUtil.verified_user()
        self.reviewer1.groups.add(self.reviewer_group)

        self.reviewer2 = TestUtil.another_verified_user()
        self.reviewer2.groups.add(self.reviewer_group)

        self.author = TestUtil.other_verified_user()
        self.author.groups.add(self.contributor_group)

        self.non_reviewer = TestUtil.random_user()

        self.article1 = Article.objects.create(
            title="Test Article 1",
            content="Content 1",
            author=self.author,
            status=ArticleStatusChoices.UNDER_REVIEW,
        )

        self.article2 = Article.objects.create(
            title="Test Article 2",
            content="Content 2",
            author=self.author,
            status=ArticleStatusChoices.UNDER_REVIEW,
        )

        self.article3 = Article.objects.create(
            title="Test Article 3",
            content="Content 3",
            author=self.author,
            status=ArticleStatusChoices.SUBMITTED_FOR_REVIEW,
        )

        # Create reviews assigned to reviewer1
        self.review1 = ArticleReview.objects.create(
            article=self.article1,
            reviewed_by=self.reviewer1,
            status=ArticleReviewStatusChoices.PENDING,
        )

        self.review2 = ArticleReview.objects.create(
            article=self.article2,
            reviewed_by=self.reviewer1,
            status=ArticleReviewStatusChoices.IN_PROGRESS,
        )

        # Create review assigned to reviewer2
        self.review3 = ArticleReview.objects.create(
            article=self.article3,
            reviewed_by=self.reviewer2,
            status=ArticleReviewStatusChoices.PENDING,
        )

        self.url = "/api/v1/reviews/assigned/"

    def test_unauthenticated_request_returns_401(self):
        """Unauthenticated users should be denied access"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_reviewer_user_returns_403(self):
        """Users without reviewer role should be denied access"""
        self.client.force_authenticate(user=self.non_reviewer)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reviewer_can_access(self):
        """Users with reviewer role should have access"""
        self.client.force_authenticate(user=self.reviewer1)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_returns_only_reviews_assigned_to_current_reviewer(self):
        """Should return only reviews assigned to the authenticated reviewer"""
        self.client.force_authenticate(user=self.reviewer1)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Extract review IDs from response
        review_ids = [str(review["id"]) for review in response.data["data"]["results"]]

        # Should include reviewer1's reviews
        self.assertIn(str(self.review1.id), review_ids)
        self.assertIn(str(self.review2.id), review_ids)

        # Should have exactly 2 active reviews
        self.assertEqual(len(review_ids), 2)

    def test_excludes_reviews_assigned_to_other_reviewers(self):
        """Should not return reviews assigned to other reviewers"""
        self.client.force_authenticate(user=self.reviewer1)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        review_ids = [str(review["id"]) for review in response.data["data"]["results"]]

        # Should NOT include reviewer2's review
        self.assertNotIn(str(self.review3.id), review_ids)

    def test_filter_by_status_pending(self):
        """Should filter reviews by status=pending"""
        self.client.force_authenticate(user=self.reviewer1)
        response = self.client.get(
            self.url, {"status": ArticleReviewStatusChoices.PENDING}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        reviews = response.data["data"]["results"]

        # Should return only pending review
        self.assertEqual(len(reviews), 1)
        self.assertEqual(str(reviews[0]["id"]), str(self.review1.id))
        self.assertEqual(reviews[0]["status"], ArticleReviewStatusChoices.PENDING)

    def test_filter_by_status_in_progress(self):
        """Should filter reviews by status=in_progress"""
        self.client.force_authenticate(user=self.reviewer1)
        response = self.client.get(
            self.url, {"status": ArticleReviewStatusChoices.IN_PROGRESS}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        reviews = response.data["data"]["results"]

        # Should return only in_progress review
        self.assertEqual(len(reviews), 1)
        self.assertEqual(str(reviews[0]["id"]), str(self.review2.id))
        self.assertEqual(reviews[0]["status"], ArticleReviewStatusChoices.IN_PROGRESS)

    def test_filter_by_status_completed(self):
        """Should return empty when filtering by status=approved (no active approved reviews)"""
        self.client.force_authenticate(user=self.reviewer1)
        response = self.client.get(
            self.url, {"status": ArticleReviewStatusChoices.COMPLETED}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        reviews = response.data["data"]["results"]

        # Should be empty
        self.assertEqual(len(reviews), 0)

    def test_no_filter_returns_all_reviews(self):
        """Should return all active reviews when no status filter is applied"""
        self.client.force_authenticate(user=self.reviewer1)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        reviews = response.data["data"]["results"]

        # Should return all 2 active reviews
        self.assertEqual(len(reviews), 2)

    def test_response_message_correct(self):
        """Should return correct success message"""
        self.client.force_authenticate(user=self.reviewer1)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Reviews retrieved successfully", response.data["message"])

    def test_reviewer_with_no_reviews_returns_empty_list(self):
        """Reviewer with no assigned reviews should get empty list"""
        # Create a new reviewer with no reviews
        new_reviewer = User.objects.create_user(
            first_name="non",
            last_name="reviewer",
            email="newreviewer@test.com",
            password="testpass123",
        )
        new_reviewer.groups.add(self.reviewer_group)

        self.client.force_authenticate(user=new_reviewer)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]["results"]), 0)

    def test_multiple_reviewers_see_only_their_reviews(self):
        """Each reviewer should only see their own reviews"""
        # Reviewer1 sees their reviews
        self.client.force_authenticate(user=self.reviewer1)
        response1 = self.client.get(self.url)

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        reviewer1_ids = [str(r["id"]) for r in response1.data["data"]["results"]]

        # Reviewer2 sees their reviews
        self.client.force_authenticate(user=self.reviewer2)
        response2 = self.client.get(self.url)

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        reviewer2_ids = [str(r["id"]) for r in response2.data["data"]["results"]]

        # Verify no overlap
        self.assertEqual(set(reviewer1_ids) & set(reviewer2_ids), set())

        # Verify each sees correct reviews
        self.assertIn(str(self.review1.id), reviewer1_ids)
        self.assertIn(str(self.review2.id), reviewer1_ids)
        self.assertIn(str(self.review3.id), reviewer2_ids)


class ReviewDetailViewTests(APITestCase):
    """
    Test suite for ReviewDetailView endpoint.
    Tests authentication, permissions, privacy, and response format.
    """

    def setUp(self):
        """Set up test users, article, and review"""

        self.reviewer_group = Group.objects.get_or_create(name=UserRoles.REVIEWER)[0]
        self.contributor_group = Group.objects.get_or_create(
            name=UserRoles.CONTRIBUTOR
        )[0]

        self.reviewer = TestUtil.verified_user()
        self.reviewer.groups.add(self.reviewer_group)

        self.other_reviewer = TestUtil.another_verified_user()
        self.other_reviewer.groups.add(self.reviewer_group)

        self.author = TestUtil.other_verified_user()
        self.author.groups.add(self.contributor_group)

        self.random_user = TestUtil.random_user()

        # Create article
        self.article = Article.objects.create(
            title="Test Article",
            content="Test content",
            author=self.author,
            status=ArticleStatusChoices.UNDER_REVIEW,
            assigned_reviewer=self.reviewer,
        )

        # Create review
        self.review = ArticleReview.objects.create(
            article=self.article,
            reviewed_by=self.reviewer,
            status=ArticleReviewStatusChoices.IN_PROGRESS,
            reviewer_notes="Private notes for reviewer only",
        )

        self.url_template = "/api/v1/reviews/{}/"

    def test_unauthenticated_request_returns_401(self):
        """Unauthenticated users should be denied access"""
        response = self.client.get(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_assigned_reviewer_can_view_review(self):
        """Assigned reviewer should be able to view their review"""
        self.client.force_authenticate(user=self.reviewer)
        response = self.client.get(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data["data"]["id"]), str(self.review.id))

    def test_assigned_reviewer_sees_reviewer_notes(self):
        """Assigned reviewer should see their private reviewer_notes"""
        self.client.force_authenticate(user=self.reviewer)
        response = self.client.get(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["data"]["reviewer_notes"], "Private notes for reviewer only"
        )

    def test_unassigned_reviewer_cannot_view_review(self):
        """Reviewer not assigned to the review should be denied access"""
        self.client.force_authenticate(user=self.other_reviewer)
        response = self.client.get(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_article_author_can_view_review(self):
        """Article author should be able to view reviews of their article"""
        self.client.force_authenticate(user=self.author)
        response = self.client.get(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data["data"]["id"]), str(self.review.id))

    def test_article_author_does_not_see_reviewer_notes(self):
        """Article author should NOT see private reviewer_notes"""
        self.client.force_authenticate(user=self.author)
        response = self.client.get(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # reviewer_notes should be None for author
        self.assertIsNone(response.data["data"]["reviewer_notes"])

    def test_random_user_cannot_view_review(self):
        """Random user (neither reviewer nor author) should be denied access"""
        self.client.force_authenticate(user=self.random_user)
        response = self.client.get(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_review_id_returns_review(self):
        """Valid review_id should return the review"""
        self.client.force_authenticate(user=self.reviewer)
        response = self.client.get(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data["data"]["id"]), str(self.review.id))

    def test_nonexistent_review_id_returns_404(self):
        """Non-existent review_id should return 404"""
        self.client.force_authenticate(user=self.reviewer)
        fake_uuid = uuid.uuid4()
        response = self.client.get(self.url_template.format(fake_uuid))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Review not found", response.data.get("message", ""))

    def test_invalid_uuid_format_returns_404(self):
        """Invalid UUID format should return 404"""
        self.client.force_authenticate(user=self.reviewer)
        response = self.client.get(self.url_template.format("invalid-uuid"))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_response_message_correct(self):
        """Should return correct success message"""
        self.client.force_authenticate(user=self.reviewer)
        response = self.client.get(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Review retrieved successfully", response.data["message"])


# python manage.py test apps.content.tests.test_reviews.AssignedReviewsListViewTests
# python manage.py test apps.content.tests.test_reviews.ReviewDetailViewTests
# python manage.py test apps.content.tests.test_reviews.ReviewDetailViewTests
