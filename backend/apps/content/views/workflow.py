import logging
from datetime import timezone

from apps.common.errors import ErrorCode
from apps.common.exceptions import NotFoundError
from apps.common.responses import CustomResponse
from apps.content import notification_service
from apps.content.choices import ArticleReviewStatusChoices, ArticleStatusChoices
from apps.content.models import Article, ArticleReview
from apps.content.permissions import CanManageReview, CanSubmitForReview, IsContributor
from apps.content.schema_examples import ARTICLE_SUBMIT_RESPONSE_EXAMPLE
from apps.content.serializers import (
    ArticleApproveResponseSerializer,
    ArticleSubmitResponseSerializer,
    ReviewActionRequestSerializer,
    ReviewActionResponseSerializer,
    ReviewStartResponseSerializer,
)
from apps.content.utils import (
    assign_editor,
    assign_reviewer,
    create_workflow_history,
    sync_content_from_liveblocks,
)
from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

tags = ["Article Workflow"]


class ArticleSubmitView(APIView):
    """
    Submit article for review.

    Syncs content from Liveblocks, assigns reviewer, and initiates review workflow.
    """

    permission_classes = (IsContributor, CanSubmitForReview)
    serializer_class = ArticleSubmitResponseSerializer

    @extend_schema(
        summary="Submit article for review",
        description="""
        Submit an article for review by syncing content from Liveblocks editor 
        and assigning a reviewer.
        
        **Pre-conditions:**
        - Article must be in DRAFT or REJECTED or CHANGES_REQUESTED status
        - User must be the article author
        
        **Note:** For resubmissions (articles with CHANGES_REQUESTED status), 
        the same reviewer will be assigned automatically.
        """,
        tags=tags,
        responses=ARTICLE_SUBMIT_RESPONSE_EXAMPLE,
    )
    def post(self, request, article_id):
        """Submit article for review"""

        try:
            article = (
                Article.objects.select_related("author", "assigned_reviewer")
                .prefetch_related("reviews")
                .get(id=article_id)
            )
        except Article.DoesNotExist:
            raise NotFoundError("Article not found")

        self.check_object_permissions(request, article)

        if article.status not in [
            ArticleStatusChoices.DRAFT,
            ArticleStatusChoices.CHANGES_REQUESTED,
            ArticleStatusChoices.REJECTED,
        ]:
            return CustomResponse.error(
                message=f"Cannot submit article with status '{article.status}'. Must be draft, changes_requested, or rejected.",
                err_code=ErrorCode.INVALID_STATUS,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        success, error_msg = sync_content_from_liveblocks(article)
        if not success:
            return CustomResponse.error(
                message=error_msg,
                err_code=ErrorCode.SERVICE_UNAVAILABLE,
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        from apps.content.models import ArticleReview

        is_resubmission = False
        existing_review = (
            ArticleReview.objects.filter(article=article)
            .order_by("-created_at")
            .first()
        )

        try:
            with transaction.atomic():
                if existing_review:
                    # RESUBMISSION: Reactivate existing review
                    is_resubmission = True

                    existing_review.status = ArticleReviewStatusChoices.PENDING
                    existing_review.started_at = None
                    existing_review.completed_at = None
                    existing_review.save(
                        update_fields=[
                            "status",
                            "started_at",
                            "completed_at",
                            "updated_at",
                        ]
                    )

                    logger.info(
                        f"Article {article.id} resubmitted by {request.user.id} "
                        f"to reviewer {reviewer.id}"
                    )

                else:
                    # NEW SUBMISSION: Assign new reviewer
                    reviewer = assign_reviewer()

                    if not reviewer:
                        return CustomResponse.error(
                            message="No reviewers available. Please contact support.",
                            err_code=ErrorCode.SERVICE_UNAVAILABLE,
                            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        )

                    # Create new review record
                    ArticleReview.objects.create(
                        article=article,
                        reviewed_by=reviewer,
                        status=ArticleReviewStatusChoices.PENDING,
                    )
                    article.assigned_reviewer = reviewer

                    logger.info(
                        f"Article {article.id} submitted by {request.user.id} "
                        f"to reviewer {reviewer.id}"
                    )

                # Update article status
                old_status = article.status
                article.status = ArticleStatusChoices.SUBMITTED_FOR_REVIEW

                article.save(
                    update_fields=["status", "assigned_reviewer", "updated_at"]
                )

                # Create workflow history
                create_workflow_history(
                    article=article,
                    from_status=old_status,
                    to_status=ArticleStatusChoices.SUBMITTED_FOR_REVIEW,
                    changed_by=request.user,
                    notes=f"{'Resubmitted' if is_resubmission else 'Submitted'} for review",
                )

                #  Send notification email
                try:
                    notification_service.send_article_submitted_email(
                        article=article, reviewer=reviewer
                    )
                except Exception as e:
                    # Log error but don't fail the submission
                    logger.error(
                        f"Failed to send submission email for article {article.id}: {str(e)}",
                        exc_info=True,
                    )

                # Prepare response
                response_data = {
                    "status": article.status,
                    "assigned_reviewer": reviewer,
                    "is_resubmission": is_resubmission,
                }

                serializer = self.serializer_class(response_data)

                message = (
                    "Article resubmitted successfully"
                    if is_resubmission
                    else "Article submitted for review successfully"
                )

                return CustomResponse.success(
                    message=message,
                    data=serializer.data,
                    status_code=status.HTTP_201_CREATED,
                )

        except Exception as e:
            logger.error(
                f"Error submitting article {article.id}: {str(e)}", exc_info=True
            )
            return CustomResponse.error(
                message="An error occurred while submitting the article",
                err_code=ErrorCode.SERVER_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ReviewStartView(APIView):
    """Start reviewing an article"""

    permission_classes = [CanManageReview]
    serializer_class = ReviewStartResponseSerializer

    @extend_schema(
        summary="Start reviewing article",
        description="""
        Mark that reviewer has started reviewing the article.
        
        **Pre-conditions:**
        - Article status must be: submitted_for_review
        - User must be the assigned reviewer
        """,
        # responses=REVIEW_START_RESPONSE_EXAMPLE,
        tags=tags,
    )
    def post(self, request, review_id):
        """Start review"""

        try:
            review = ArticleReview.objects.select_related(
                "article", "article__author", "reviewed_by"
            ).get(id=review_id, is_active=True)
        except ArticleReview.DoesNotExist:
            raise NotFoundError("Review not found")

        article = review.article

        self.check_object_permissions(request, review)

        if article.status != ArticleStatusChoices.SUBMITTED_FOR_REVIEW:
            return CustomResponse.error(
                message=f"Cannot start review. Article status is '{article.status}', must be 'submitted_for_review'.",
                err_code=ErrorCode.INVALID_STATUS,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        try:
            with transaction.atomic():
                old_status = article.status

                article.status = ArticleStatusChoices.UNDER_REVIEW
                article.save()

                review.status = ArticleReviewStatusChoices.IN_PROGRESS
                review.started_at = timezone.now()
                review.save()

                create_workflow_history(
                    article=article,
                    from_status=old_status,
                    to_status=article.status,
                    changed_by=request.user,
                    notes=f"Review started by {request.user.full_name()}",
                )

                try:
                    notification_service.send_review_started_email(article)
                except Exception as e:
                    logger.error(f"Failed to send review started email: {str(e)}")

                response_data = {
                    "review_status": review.status,
                    "article_status": article.status,
                    "started_at": review.started_at,
                }

                serializer = self.serializer_class(response_data)

                return CustomResponse.success(
                    message="Review started successfully",
                    data=serializer.data,
                    status_code=status.HTTP_200_OK,
                )

        except Exception as e:
            logger.error(f"Error starting review {review_id}: {str(e)}", exc_info=True)
            return CustomResponse.error(
                message="Failed to start review. Please try again.",
                err_code=ErrorCode.OPERATION_FAILED,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ReviewRequestChangesView(APIView):
    """Request changes to article"""

    permission_classes = [CanManageReview]
    serializer_class = ReviewActionResponseSerializer

    @extend_schema(
        summary="Request changes to article",
        description="""
        Reviewer requests changes from the contributor.
        
        **Pre-conditions:**
        - Article status must be: under_review
        - User must be the assigned reviewer
        
        **Note:** All feedback is provided via Liveblocks comments, not stored here.
        """,
        # request=ReviewActionRequestSerializer,
        # responses={
        #     200: ReviewActionResponseSerializer,
        # },
        tags=tags,
    )
    def post(self, request, review_id):
        """Request changes"""
        try:
            review = ArticleReview.objects.select_related(
                "article", "article__author", "reviewed_by"
            ).get(id=review_id, is_active=True)
        except ArticleReview.DoesNotExist:
            raise NotFoundError("Review not found")

        article = review.article

        self.check_object_permissions(request, review)

        if article.status != ArticleStatusChoices.UNDER_REVIEW:
            return CustomResponse.error(
                message=f"Cannot request changes. Article status is '{article.status}', must be 'under_review'.",
                err_code=ErrorCode.INVALID_STATUS,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        serializer = ReviewActionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                old_status = article.status

                article.status = ArticleStatusChoices.CHANGES_REQUESTED
                article.save()

                # Update review
                review.status = ArticleReviewStatusChoices.COMPLETED
                review.completed_at = timezone.now()
                review.reviewer_notes = serializer.validated_data.get(
                    "reviewer_notes", None
                )
                review.save()

                # Create workflow history
                create_workflow_history(
                    article=article,
                    from_status=old_status,
                    to_status=article.status,
                    changed_by=request.user,
                    notes="Changes requested by reviewer",
                )

                # Send email notification
                try:
                    notification_service.send_changes_requested_email(article)
                except Exception as e:
                    logger.error(f"Failed to send changes requested email: {str(e)}")

                response_data = {
                    "article_status": article.status,
                    "completed_at": review.completed_at,
                }

                response_serializer = self.serializer_class(response_data)

                return CustomResponse.success(
                    message="Changes requested successfully. Author has been notified.",
                    data=response_serializer.data,
                    status_code=status.HTTP_200_OK,
                )

        except Exception as e:
            logger.error(
                f"Error requesting changes for review {review_id}: {str(e)}",
                exc_info=True,
            )
            return CustomResponse.error(
                message="Failed to request changes. Please try again.",
                err_code=ErrorCode.OPERATION_FAILED,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ReviewApproveView(APIView):
    """Approve article for publishing"""

    permission_classes = [CanManageReview]
    serializer_class = ArticleApproveResponseSerializer

    @extend_schema(
        summary="Approve article",
        description="""
        Reviewer approves article, marking it ready for publishing.
        
        **Pre-conditions:**
        - Article status must be: under_review
        - User must be the assigned reviewer
        """,
        # request=ReviewActionRequestSerializer,
        # responses={
        #     200: ArticleApproveResponseSerializer,
        # },
        tags=tags,
    )
    def post(self, request, review_id):
        """Approve article"""
        try:
            review = ArticleReview.objects.select_related(
                "article", "article__author", "reviewed_by"
            ).get(id=review_id, is_active=True)
        except ArticleReview.DoesNotExist:
            raise NotFoundError("Review not found")

        article = review.article

        self.check_object_permissions(request, review)

        if article.status != ArticleStatusChoices.UNDER_REVIEW:
            return CustomResponse.error(
                message=f"Cannot approve. Article status is '{article.status}', must be 'under_review'.",
                err_code=ErrorCode.INVALID_STATUS,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        serializer = ReviewActionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                old_status = article.status

                # Auto-assign editor
                editor = assign_editor()

                if not editor:
                    return CustomResponse.error(
                        message="No editors available. Please contact support.",
                        err_code=ErrorCode.SERVICE_UNAVAILABLE,
                        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    )

                article.status = ArticleStatusChoices.READY
                article.assigned_editor = editor
                article.save()

                review.status = ArticleReviewStatusChoices.COMPLETED
                review.completed_at = timezone.now()
                review.is_active = False
                review.reviewer_notes = serializer.validated_data.get(
                    "reviewer_notes", None
                )
                review.save()

                create_workflow_history(
                    article=article,
                    from_status=old_status,
                    to_status=article.status,
                    changed_by=request.user,
                    notes=f"Approved by reviewer, assigned to editor {editor.full_name()}",
                )

                try:
                    notification_service.send_article_approved_email(article)
                except Exception as e:
                    logger.error(f"Failed to send approval emails: {str(e)}")

                response_data = {
                    "article_status": article.status,
                    "assigned_editor": editor,
                    "completed_at": review.completed_at,
                }

                response_serializer = self.serializer_class(response_data)

                return CustomResponse.success(
                    message="Article approved successfully. Editor has been assigned.",
                    data=response_serializer.data,
                    status_code=status.HTTP_200_OK,
                )

        except Exception as e:
            logger.error(
                f"Error approving article for review {review_id}: {str(e)}",
                exc_info=True,
            )
            return CustomResponse.error(
                message="Failed to approve article. Please try again.",
                err_code=ErrorCode.OPERATION_FAILED,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ReviewRejectView(APIView):
    """Reject article"""

    permission_classes = [CanManageReview]
    serializer_class = ReviewActionResponseSerializer

    @extend_schema(
        summary="Reject article",
        description="""
        Reviewer rejects article.
        
        **Pre-conditions:**
        - Article status must be: under_review
        - User must be the assigned reviewer
        
        **Note:** Author can resubmit after making changes.
        """,
        # request=ReviewActionRequestSerializer,
        # responses={
        #     200: ReviewActionResponseSerializer,
        # },
        tags=tags,
    )
    def post(self, request, review_id):
        """Reject article"""
        try:
            review = ArticleReview.objects.select_related(
                "article", "article__author", "reviewed_by"
            ).get(id=review_id, is_active=True)
        except ArticleReview.DoesNotExist:
            raise NotFoundError("Review not found")

        article = review.article

        self.check_object_permissions(request, review)

        if article.status != ArticleStatusChoices.UNDER_REVIEW:
            return CustomResponse.error(
                message=f"Cannot reject. Article status is '{article.status}', must be 'under_review'.",
                err_code=ErrorCode.INVALID_STATUS,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        serializer = ReviewActionRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reviewer_notes = serializer.validated_data.get("reviewer_notes", None)

        try:
            with transaction.atomic():
                old_status = article.status

                article.status = ArticleStatusChoices.REJECTED
                article.save()

                review.status = ArticleReviewStatusChoices.COMPLETED
                review.completed_at = timezone.now()
                if reviewer_notes:
                    review.reviewer_notes = reviewer_notes
                review.save()

                create_workflow_history(
                    article=article,
                    from_status=old_status,
                    to_status=article.status,
                    changed_by=request.user,
                    notes="Article rejected by reviewer",
                )

                try:
                    notification_service.send_article_rejected_email(article)
                except Exception as e:
                    logger.error(f"Failed to send rejection email: {str(e)}")

                response_data = {
                    "article_status": article.status,
                    "completed_at": review.completed_at,
                }

                response_serializer = self.serializer_class(response_data)

                return CustomResponse.success(
                    message="Article rejected. Author has been notified.",
                    data=response_serializer.data,
                    status_code=status.HTTP_200_OK,
                )
        except Exception as e:
            logger.error(
                f"Error rejecting article for review {review_id}: {str(e)}",
                exc_info=True,
            )
            return CustomResponse.error(
                message="Failed to reject article. Please try again.",
                err_code=ErrorCode.OPERATION_FAILED,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            logger.error(
                f"Error rejecting article for review {review_id}: {str(e)}",
                exc_info=True,
            )
            return CustomResponse.error(
                message="Failed to reject article. Please try again.",
                err_code=ErrorCode.OPERATION_FAILED,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
