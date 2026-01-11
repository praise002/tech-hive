from apps.common.exceptions import NotFoundError
from apps.common.pagination import DefaultPagination
from apps.common.responses import CustomResponse
from apps.content.filters import ReviewListFilter
from apps.content.models import ArticleReview
from apps.content.permissions import CanViewReview, IsReviewer
from apps.content.schema_examples import (
    ASSIGNED_REVIEWS_LIST_RESPONSE_EXAMPLE,
    REVIEW_DETAIL_RESPONSE_EXAMPLE,
)
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
            ArticleReview.objects.filter(reviewed_by=user)
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
        responses=ASSIGNED_REVIEWS_LIST_RESPONSE_EXAMPLE,
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
        responses=REVIEW_DETAIL_RESPONSE_EXAMPLE,
        tags=tags,
    )
    def get(self, request, review_id):
        """
        GET endpoint for review detail
        """
        try:
            review = (
                ArticleReview.objects.select_related(
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
                .get(id=review_id)
            )
        except ArticleReview.DoesNotExist:
            raise NotFoundError("Review not found")

        self.check_object_permissions(request, review)

        serializer = self.serializer_class(review, context={'request': request})
        return CustomResponse.success(
            message="Review retrieved successfully",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


# TODO:
# Do more research on whetehr to put input or output serializer in the serializer_class
