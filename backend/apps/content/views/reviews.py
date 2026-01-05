from apps.common.exceptions import NotFoundError
from apps.common.pagination import DefaultPagination
from apps.common.responses import CustomResponse
from apps.content.filters import ReviewListFilter
from apps.content.models import ArticleReview
from apps.content.permissions import CanViewReview, IsReviewer
from apps.content.schema_examples import ASSIGNED_REVIEWS_LIST_RESPONSE_EXAMPLE
from apps.content.serializers import ReviewDetailSerializer, ReviewListSerializer
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

tags = ["Reviews"]


class AssignedReviewsListView(ListAPIView):
    """
    List all reviews assigned to the current reviewer.

    GET /api/reviews/assigned/

    Query Parameters:
    - status: Filter by review status (pending, in_progress, approved, etc.)
    - article_status: Filter by article status (submitted_for_review, under_review, etc.)
    """

    serializer_class = ReviewListSerializer
    permission_classes = [IsReviewer]
    pagination_class = DefaultPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ReviewListFilter

    def get_queryset(self):
        """
        Filter reviews assigned to current user with optional status filters
        """
        if getattr(self, "swagger_fake_view", False):
            return ArticleReview.objects.none()
        user = self.request.user

        queryset = (
            ArticleReview.objects.filter(reviewed_by=user, is_active=True)
            .select_related(
                "article", "article__author", "article__category", "reviewed_by"
            )
            .order_by("-created_at")
        )

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Override list to use CustomResponse format
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data)
            return CustomResponse.success(
                message="Reviews retrieved successfully",
                data=paginated_data.data,
                status_code=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(queryset, many=True)

        return CustomResponse.success(
            message="Reviews retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="List assigned reviews",
        description="""
        Returns all reviews assigned to the authenticated reviewer.
        
        **Filtering:**
        - Use `?status=in_progress` to filter by review status
        - Use `?article_status=under_review` to filter by article status
        - Combine filters: `?status=pending&article_status=submitted_for_review`
        """,
        # responses=ASSIGNED_REVIEWS_LIST_RESPONSE_EXAMPLE,
        tags=tags,
    )
    def get(self, request, *args, **kwargs):
        """
        GET endpoint for listing reviews
        """
        return self.list(request, *args, **kwargs)


class ReviewDetailView(APIView):
    """
    Get detailed review information.

    GET /api/reviews/{review_id}/

    Permissions:
    - Reviewer can view their own reviews (including private notes)
    - Article author can view reviews of their articles (no private notes)
    """

    serializer_class = ReviewDetailSerializer
    permission_classes = [CanViewReview]

    @extend_schema(
        summary="Get review details",
        description="""
        Returns detailed information about a specific review.

        **Access Control:**
        - Reviewers can see their own reviews (including `reviewer_notes`)
        - Article authors can see reviews of their articles (no `reviewer_notes`)
        """,
        # responses={
        #     200: OpenApiExample(
        #         'Success Response',
        #         value={
        #             "status": "success",
        #             "message": "Review retrieved successfully",
        #             "data": {
        #                 "id": 1,
        #                 "article": {
        #                     "id": 123,
        #                     "title": "Introduction to Django Signals",
        #                     "slug": "introduction-to-django-signals",
        #                     "content": "<p>Django signals allow...</p>",
        #                     "cover_image_url": "https://example.com/media/articles/cover.jpg",
        #                     "status": "under_review",
        #                     "author": {
        #                         "id": 5,
        #                         "username": "john_doe",
        #                         "full_name": "John Doe"
        #                     },
        #                     "assigned_reviewer": {
        #                         "id": 8,
        #                         "username": "jane_reviewer",
        #                         "full_name": "Jane Reviewer"
        #                     },
        #                     "assigned_editor": None,
        #                     "category": "Backend Development",
        #                     "tags": ["django", "python", "signals"],
        #                     "is_featured": False,
        #                     "created_at": "2024-01-01T10:00:00Z",
        #                     "updated_at": "2024-01-05T14:30:00Z",
        #                     "published_at": None,
        #                     "liveblocks_room_id": "article-123",
        #                     "content_last_synced_at": "2024-01-05T14:30:00Z"
        #                 },
        #                 "reviewed_by": {
        #                     "id": 8,
        #                     "username": "jane_reviewer",
        #                     "full_name": "Jane Reviewer"
        #                 },
        #                 "status": "in_progress",
        #                 "started_at": "2024-01-05T09:00:00Z",
        #                 "completed_at": None,
        #                 "reviewer_notes": "Checking technical accuracy and code examples",
        #                 "workflow_history": [
        #                     {
        #                         "id": 45,
        #                         "from_status": "draft",
        #                         "to_status": "submitted_for_review",
        #                         "changed_by": {
        #                             "id": 5,
        #                             "username": "john_doe",
        #                             "full_name": "John Doe"
        #                         },
        #                         "changed_at": "2024-01-05T08:00:00Z",
        #                         "notes": "Ready for review"
        #                     }
        #                 ],
        #                 "created_at": "2024-01-05T08:00:00Z",
        #                 "updated_at": "2024-01-05T09:00:00Z"
        #             }
        #         }
        #     ),
        #     403: OpenApiExample(
        #         'Access Denied',
        #         value={
        #             "status": "failure",
        #             "message": "You don't have permission to view this review",
        #             "code": "forbidden"
        #         }
        #     ),
        #     404: OpenApiExample(
        #         'Not Found',
        #         value={
        #             "status": "failure",
        #             "message": "Review not found",
        #             "code": "non_existent"
        #         }
        #     )
        # },
        tags=tags,
    )
    def get(self, request, review_id):
        """
        GET endpoint for review detail
        """
        try:
            review = (
                ArticleReview.objects.filter(is_active=True)
                .select_related(
                    "article",
                    "article__author",
                    "article__assigned_reviewer",
                    "article__assigned_editor",
                    "article__category",
                    "reviewed_by",
                )
                .prefetch_related(
                    "article__tags",
                )
                .get(pk=review_id)
            )
        except ArticleReview.DoesNotExist:
            raise NotFoundError("Review not found")

        self.check_object_permissions(request, review)

        serializer = self.serializer_class(review)
        return CustomResponse.success(
            message="Review retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


# TODO:
# Still deliberating on is_active in ArticleReview
# Review Cycles Are Iterative
# One review process can span multiple rounds: Submission → Review → Changes Requested → Resubmission → Review Again → Approval/Rejection
# The same reviewer typically handles all rounds for continuity
# Reviews stay "active" until the article is published or rejected
# When Reviews Actually Become Inactive
# Article published/rejected: Process complete
# Timeout due to inactivity: No resubmission after 30-60 days
# Manual intervention: Editor reassigns reviewer

# Example management command
# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from apps.content.models import ArticleReview

# class Command(BaseCommand):
#     help = 'Deactivate stale reviews after 30 days of inactivity'

#     def handle(self, *args, **options):
#         cutoff = timezone.now() - timezone.timedelta(days=30)

#         stale_reviews = ArticleReview.objects.filter(
#             is_active=True,
#             updated_at__lt=cutoff,
#             article__status__in=['changes_requested', 'draft']
#         )

#         for review in stale_reviews:
#             review.is_active = False
#             review.article.assigned_reviewer = None
#             review.article.save()
#             review.save()

#         self.stdout.write(f'Deactivated {stale_reviews.count()} stale reviews')

# TODO:
# Do more research on whetehr to put input or output serializer in the serializer_class
# Should an error be returned when no assigned reviewer and editor or it should go through
# and admin is alerted
# and admin is alerted
