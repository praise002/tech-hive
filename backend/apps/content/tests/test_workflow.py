from unittest.mock import patch

from apps.accounts.utils import UserRoles
from apps.common.utils import TestUtil
from apps.content.choices import ArticleReviewStatusChoices, ArticleStatusChoices
from apps.content.models import Article, ArticleReview, ArticleWorkflowHistory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class ArticleSubmitViewTests(APITestCase):
    """
    Test suite for ArticleSubmitView - Article submission workflow.
    Covers new submissions and resubmissions.
    """

    def setUp(self):
        """Set up test users, groups, and articles"""
        self.contributor_group = Group.objects.get_or_create(
            name=UserRoles.CONTRIBUTOR
        )[0]
        self.reviewer_group = Group.objects.get_or_create(name=UserRoles.REVIEWER)[0]
        self.editor_group = Group.objects.get_or_create(name=UserRoles.EDITOR)[0]

        self.author = TestUtil.verified_user()
        self.author.groups.add(self.contributor_group)

        self.other_author = TestUtil.another_verified_user()
        self.other_author.groups.add(self.contributor_group)

        self.reviewer = TestUtil.other_verified_user()
        self.reviewer.groups.add(self.reviewer_group)

        self.editor = TestUtil.random_user()
        self.editor.groups.add(self.editor_group)

        self.draft_article = Article.objects.create(
            title="Draft Article",
            content="Draft content",
            author=self.author,
            status=ArticleStatusChoices.DRAFT,
        )

        self.url_template = "/api/v1/articles/{}/submit/"

    def test_unauthenticated_request_returns_401(self):
        """Unauthenticated users should be denied access"""
        response = self.client.get(self.url_template.format(self.draft_article.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_contributor_not_author_returns_403(self):
        """Contributor who is not the article author should be denied"""
        self.client.force_authenticate(user=self.other_author)
        response = self.client.post(self.url_template.format(self.draft_article.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("apps.content.views.workflow.sync_content_from_liveblocks")
    @patch("apps.content.views.workflow.assign_reviewer")
    @patch("apps.content.views.workflow.assign_editor")
    @patch("apps.content.views.workflow.notification_service")
    def test_can_submit_from_draft_status(
        self, mock_notif, mock_editor, mock_reviewer, mock_sync
    ):
        """Should allow submission from DRAFT status"""
        mock_sync.return_value = (True, None)
        mock_reviewer.return_value = self.reviewer
        mock_editor.return_value = self.editor

        self.client.force_authenticate(user=self.author)
        response = self.client.post(self.url_template.format(self.draft_article.id))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_submit_from_under_review_status(self):
        """Should reject submission from UNDER_REVIEW status"""
        self.draft_article.status = ArticleStatusChoices.UNDER_REVIEW
        self.draft_article.save()

        self.client.force_authenticate(user=self.author)
        response = self.client.post(self.url_template.format(self.draft_article.id))

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn("Cannot submit article", response.data.get("message", ""))

    def test_cannot_submit_from_published_status(self):
        """Should reject submission from PUBLISHED status"""
        self.draft_article.status = ArticleStatusChoices.PUBLISHED
        self.draft_article.save()

        self.client.force_authenticate(user=self.author)
        response = self.client.post(self.url_template.format(self.draft_article.id))

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    @patch("apps.content.views.workflow.sync_content_from_liveblocks")
    def test_sync_failure_returns_503(self, mock_sync):
        """Liveblocks sync failure should return 503 error"""
        mock_sync.return_value = (False, "Failed to fetch Liveblocks content")

        self.client.force_authenticate(user=self.author)
        response = self.client.post(self.url_template.format(self.draft_article.id))

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertIn(
            "Failed to fetch Liveblocks content", response.data.get("message", "")
        )

    @patch("apps.content.views.workflow.notification_service")
    @patch("apps.content.views.workflow.sync_content_from_liveblocks")
    @patch("apps.content.views.workflow.assign_reviewer")
    @patch("apps.content.views.workflow.assign_editor")
    def test_new_submission_creates_review_and_assigns_users(
        self, mock_editor, mock_reviewer, mock_sync, mock_notif
    ):
        """New submission should create review and assign reviewer/editor"""
        mock_sync.return_value = (True, None)
        mock_reviewer.return_value = self.reviewer
        mock_editor.return_value = self.editor

        initial_count = ArticleReview.objects.count()

        self.client.force_authenticate(user=self.author)
        response = self.client.post(self.url_template.format(self.draft_article.id))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify review created
        self.assertEqual(ArticleReview.objects.count(), initial_count + 1)

        # Verify article updated
        self.draft_article.refresh_from_db()
        self.assertEqual(
            self.draft_article.status, ArticleStatusChoices.SUBMITTED_FOR_REVIEW
        )
        # self.assertEqual(self.draft_article.assigned_reviewer, self.reviewer)
        # self.assertEqual(self.draft_article.assigned_editor, self.editor)

        # Verify response
        # self.assertFalse(response.data["data"]["is_resubmission"])
        # self.assertIn("assigned_reviewer", response.data["data"])
        # self.assertIn("assigned_editor", response.data["data"])

    @patch("apps.content.views.workflow.notification_service")
    @patch("apps.content.views.workflow.sync_content_from_liveblocks")
    def test_resubmission_reactivates_existing_review(self, mock_sync, mock_notif):
        """Resubmission should reactivate existing review instead of creating new"""
        mock_sync.return_value = (True, None)

        # Create existing completed review
        existing_review = ArticleReview.objects.create(
            article=self.draft_article,
            reviewed_by=self.reviewer,
            status=ArticleReviewStatusChoices.COMPLETED,
            started_at=timezone.now(),
            completed_at=timezone.now(),
        )

        self.draft_article.status = ArticleStatusChoices.CHANGES_REQUESTED
        self.draft_article.save()

        initial_count = ArticleReview.objects.count()

        self.client.force_authenticate(user=self.author)
        response = self.client.post(self.url_template.format(self.draft_article.id))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Should NOT create new review
        self.assertEqual(ArticleReview.objects.count(), initial_count)

        # Verify review reactivated
        existing_review.refresh_from_db()
        self.assertEqual(existing_review.status, ArticleReviewStatusChoices.PENDING)
        self.assertIsNone(existing_review.started_at)
        self.assertIsNone(existing_review.completed_at)

        # Verify response
        self.assertTrue(response.data["data"]["is_resubmission"])

    @patch("apps.content.views.workflow.notification_service")
    @patch("apps.content.views.workflow.sync_content_from_liveblocks")
    @patch("apps.content.views.workflow.assign_reviewer")
    @patch("apps.content.views.workflow.assign_editor")
    def test_no_reviewers_available_sends_alert_but_continues(
        self, mock_editor, mock_reviewer, mock_sync, mock_notif
    ):
        """Should send admin alert when no reviewers available but continue submission"""
        mock_sync.return_value = (True, None)
        mock_reviewer.return_value = None  # No reviewer available
        mock_editor.return_value = self.editor

        self.client.force_authenticate(user=self.author)
        response = self.client.post(self.url_template.format(self.draft_article.id))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify alert was sent
        mock_notif.send_assignment_failure_alert.assert_called_once()

        # Article still submitted but without reviewer
        self.draft_article.refresh_from_db()
        self.assertEqual(
            self.draft_article.status, ArticleStatusChoices.SUBMITTED_FOR_REVIEW
        )
        self.assertIsNone(self.draft_article.assigned_reviewer)


class ReviewStartViewTests(APITestCase):
    """Test suite for ReviewStartView - Starting a review"""

    def setUp(self):
        """Set up test data"""
        self.reviewer_group = Group.objects.get_or_create(name=UserRoles.REVIEWER)[0]

        self.author = TestUtil.verified_user()

        self.reviewer = TestUtil.other_verified_user()
        self.reviewer.groups.add(self.reviewer_group)

        self.other_reviewer = TestUtil.another_verified_user()
        self.other_reviewer.groups.add(self.reviewer_group)

        self.article = Article.objects.create(
            title="Test Article",
            content="Content",
            author=self.author,
            status=ArticleStatusChoices.SUBMITTED_FOR_REVIEW,
        )

        self.review = ArticleReview.objects.create(
            article=self.article,
            reviewed_by=self.reviewer,
            status=ArticleReviewStatusChoices.PENDING,
        )

        self.url_template = "/api/v1/reviews/{}/start/"

    def test_unauthenticated_request_returns_401(self):
        """Unauthenticated users should be denied"""
        response = self.client.post(self.url_template.format(self.review.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reviewer_not_assigned_returns_403(self):
        """Reviewer not assigned to this review should be denied"""
        self.client.force_authenticate(user=self.other_reviewer)
        response = self.client.post(self.url_template.format(self.review.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch("apps.content.views.workflow.notification_service")
    def test_can_start_from_submitted_status(self, mock_notif):
        """Should allow starting review from SUBMITTED_FOR_REVIEW status"""
        self.client.force_authenticate(user=self.reviewer)
        response = self.client.post(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_start_from_draft_status(self):
        """Should reject starting review from DRAFT status"""
        self.article.status = ArticleStatusChoices.DRAFT
        self.article.save()

        self.client.force_authenticate(user=self.reviewer)
        response = self.client.post(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn("Cannot start review", response.data.get("message", ""))

    def test_cannot_start_from_under_review_status(self):
        """Should reject starting review from UNDER_REVIEW status (already started)"""
        self.article.status = ArticleStatusChoices.UNDER_REVIEW
        self.article.save()

        self.client.force_authenticate(user=self.reviewer)
        response = self.client.post(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    @patch("apps.content.views.workflow.notification_service")
    def test_updates_article_and_review_status(self, mock_notif):
        """Should update both article and review status correctly"""
        self.client.force_authenticate(user=self.reviewer)
        response = self.client.post(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify article status
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, ArticleStatusChoices.UNDER_REVIEW)

        # Verify review status
        self.review.refresh_from_db()
        self.assertEqual(self.review.status, ArticleReviewStatusChoices.IN_PROGRESS)
        self.assertIsNotNone(self.review.started_at)

        # Verify workflow history created
        history = ArticleWorkflowHistory.objects.filter(article=self.article).latest(
            "created_at"
        )
        self.assertEqual(history.to_status, ArticleStatusChoices.UNDER_REVIEW)

    @patch("apps.content.views.workflow.notification_service")
    def test_response_format(self, mock_notif):
        """Should return correct response format"""
        self.client.force_authenticate(user=self.reviewer)
        response = self.client.post(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Review started successfully")
        self.assertIn("review_status", response.data["data"])
        self.assertIn("article_status", response.data["data"])
        self.assertIn("started_at", response.data["data"])


class ReviewRequestChangesViewTests(APITestCase):
    """Test suite for ReviewRequestChangesView - Requesting changes"""

    def setUp(self):
        """Set up test data"""
        self.reviewer_group = Group.objects.get_or_create(name=UserRoles.REVIEWER)[0]

        self.author = TestUtil.verified_user()

        self.reviewer = TestUtil.other_verified_user()
        self.reviewer.groups.add(self.reviewer_group)

        self.article = Article.objects.create(
            title="Test Article",
            content="Content",
            author=self.author,
            status=ArticleStatusChoices.UNDER_REVIEW,
        )

        self.review = ArticleReview.objects.create(
            article=self.article,
            reviewed_by=self.reviewer,
            status=ArticleReviewStatusChoices.IN_PROGRESS,
        )

        self.url_template = "/api/v1/reviews/{}/request-changes/"

    @patch("apps.content.views.workflow.notification_service")
    def test_can_request_changes_from_under_review(self, mock_notif):
        """Should allow requesting changes from UNDER_REVIEW status"""
        self.client.force_authenticate(user=self.reviewer)
        response = self.client.post(
            self.url_template.format(self.review.id), {"reviewer_notes": "Please fix X"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_request_changes_from_draft(self):
        """Should reject requesting changes from DRAFT status"""
        self.article.status = ArticleStatusChoices.DRAFT
        self.article.save()

        self.client.force_authenticate(user=self.reviewer)
        response = self.client.post(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    @patch("apps.content.views.workflow.notification_service")
    def test_updates_statuses_and_saves_notes(self, mock_notif):
        """Should update article/review status and save reviewer notes"""
        notes = "Please improve the introduction"

        self.client.force_authenticate(user=self.reviewer)
        response = self.client.post(
            self.url_template.format(self.review.id), {"reviewer_notes": notes}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify article status
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, ArticleStatusChoices.CHANGES_REQUESTED)

        # Verify review status
        self.review.refresh_from_db()
        self.assertEqual(self.review.status, ArticleReviewStatusChoices.COMPLETED)
        self.assertIsNotNone(self.review.completed_at)
        self.assertEqual(self.review.reviewer_notes, notes)

    @patch("apps.content.views.workflow.notification_service")
    def test_response_format(self, mock_notif):
        """Should return correct response format"""
        self.client.force_authenticate(user=self.reviewer)
        response = self.client.post(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            "Changes requested successfully. Author has been notified.",
            response.data["message"],
        )
        self.assertIn("article_status", response.data["data"])
        self.assertIn("completed_at", response.data["data"])


class ReviewApproveViewTests(APITestCase):
    """Test suite for ReviewApproveView - Approving articles"""

    def setUp(self):
        """Set up test data"""
        self.reviewer_group = Group.objects.get_or_create(name=UserRoles.REVIEWER)[0]

        self.author = TestUtil.verified_user()

        self.reviewer = TestUtil.other_verified_user()
        self.reviewer.groups.add(self.reviewer_group)

        self.article = Article.objects.create(
            title="Test Article",
            content="Content",
            author=self.author,
            status=ArticleStatusChoices.UNDER_REVIEW,
        )

        self.review = ArticleReview.objects.create(
            article=self.article,
            reviewed_by=self.reviewer,
            status=ArticleReviewStatusChoices.IN_PROGRESS,
        )

        self.url_template = "/api/v1/reviews/{}/approve/"

    @patch("apps.content.views.workflow.notification_service")
    def test_can_approve_from_under_review(self, mock_notif):
        """Should allow approving from UNDER_REVIEW status"""
        self.client.force_authenticate(user=self.reviewer)
        response = self.client.post(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_approve_from_draft(self):
        """Should reject approving from DRAFT status"""
        self.article.status = ArticleStatusChoices.DRAFT
        self.article.save()

        self.client.force_authenticate(user=self.reviewer)
        response = self.client.post(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    @patch("apps.content.views.workflow.notification_service")
    def test_updates_article_to_ready_status(self, mock_notif):
        """Should update article status to READY (ready_for_publishing)"""
        self.client.force_authenticate(user=self.reviewer)
        response = self.client.post(
            self.url_template.format(self.review.id), {"reviewer_notes": "Looks good!"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify article status
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, ArticleStatusChoices.READY)

        # Verify review status
        self.review.refresh_from_db()
        self.assertEqual(self.review.status, ArticleReviewStatusChoices.COMPLETED)
        self.assertIsNotNone(self.review.completed_at)
        self.assertEqual(self.review.reviewer_notes, "Looks good!")

    @patch("apps.content.views.workflow.notification_service")
    def test_response_format(self, mock_notif):
        """Should return correct response format"""
        self.client.force_authenticate(user=self.reviewer)
        response = self.client.post(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Article approved successfully", response.data["message"])
        self.assertIn("article_status", response.data["data"])
        self.assertIn("completed_at", response.data["data"])


class ReviewRejectViewTests(APITestCase):
    """Test suite for ReviewRejectView - Rejecting articles"""

    def setUp(self):
        """Set up test data"""
        self.reviewer_group = Group.objects.get_or_create(name=UserRoles.REVIEWER)[0]

        self.author = TestUtil.verified_user()

        self.reviewer = TestUtil.another_verified_user()
        self.reviewer.groups.add(self.reviewer_group)

        self.article = Article.objects.create(
            title="Test Article",
            content="Content",
            author=self.author,
            status=ArticleStatusChoices.UNDER_REVIEW,
        )

        self.review = ArticleReview.objects.create(
            article=self.article,
            reviewed_by=self.reviewer,
            status=ArticleReviewStatusChoices.IN_PROGRESS,
        )

        self.url_template = "/api/v1/reviews/{}/reject/"

    @patch("apps.content.views.workflow.notification_service")
    def test_can_reject_from_under_review(self, mock_notif):
        """Should allow rejecting from UNDER_REVIEW status"""
        self.client.force_authenticate(user=self.reviewer)
        response = self.client.post(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_reject_from_published(self):
        """Should reject from PUBLISHED status"""
        self.article.status = ArticleStatusChoices.PUBLISHED
        self.article.save()

        self.client.force_authenticate(user=self.reviewer)
        response = self.client.post(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    @patch("apps.content.views.workflow.notification_service")
    def test_updates_article_to_rejected_status(self, mock_notif):
        """Should update article status to REJECTED"""
        notes = "Does not meet quality standards"

        self.client.force_authenticate(user=self.reviewer)
        response = self.client.post(
            self.url_template.format(self.review.id), {"reviewer_notes": notes}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify article status
        self.article.refresh_from_db()
        self.assertEqual(self.article.status, ArticleStatusChoices.REJECTED)

        # Verify review status
        self.review.refresh_from_db()
        self.assertEqual(self.review.status, ArticleReviewStatusChoices.COMPLETED)
        self.assertIsNotNone(self.review.completed_at)
        self.assertEqual(self.review.reviewer_notes, notes)

    @patch("apps.content.views.workflow.notification_service")
    def test_response_format(self, mock_notif):
        """Should return correct response format"""
        self.client.force_authenticate(user=self.reviewer)
        response = self.client.post(self.url_template.format(self.review.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["message"], "Article rejected. Author has been notified."
        )
        self.assertIn("article_status", response.data["data"])
        self.assertIn("completed_at", response.data["data"])


# python manage.py test apps.content.tests.test_workflow.ArticleSubmitViewTests# python manage.py test apps.content.tests.test_workflow.ArticleSubmitViewTests
# python manage.py test apps.content.tests.test_workflow.ReviewStartViewTests
# python manage.py test apps.content.tests.test_workflow.ReviewRequestChangesViewTests
# python manage.py test apps.content.tests.test_workflow.ReviewApproveViewTests
# python manage.py test apps.content.tests.test_workflow.ReviewRejectViewTests
