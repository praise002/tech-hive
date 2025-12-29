import logging
from datetime import timezone

from apps.accounts.utils import UserRoles
from apps.common.errors import ErrorCode
from apps.common.exceptions import NotFoundError
from apps.common.pagination import DefaultPagination
from apps.common.responses import CustomResponse
from apps.content import notification_service
from apps.content.choices import ArticleReviewStatusChoices, ArticleStatusChoices
from apps.content.models import Article, ArticleReview, Comment, Tag
from apps.content.permissions import (
    CanManageReview,
    CanSubmitForReview,
    IsAuthorOrReadOnly,
    IsCommentAuthor,
    IsContributor,
)
from apps.content.schema_examples import (
    ACCEPT_GUIDELINES_RESPONSE_EXAMPLE,
    ARTICLE_DETAIL_RESPONSE_EXAMPLE,
    ARTICLE_EDITOR_EXAMPLE,
    ARTICLE_EDITOR_RESPONSE_EXAMPLE,
    ARTICLE_LIST_RESPONSE_EXAMPLE,
    ARTICLE_SUBMIT_RESPONSE_EXAMPLE,
    ARTICLE_SUMMARY_RESPONSE_EXAMPLE,
    COMMENT_CREATE_RESPONSE_EXAMPLE,
    COMMENT_LIKE_STATUS_RESPONSE_EXAMPLE,
    COMMENT_LIKE_TOGGLE_RESPONSE_EXAMPLE,
    COVER_IMAGE_RESPONSE_EXAMPLE,
    REVIEW_START_RESPONSE_EXAMPLE,
    RSS_RESPONSE_EXAMPLE,
    TAG_RESPONSE_EXAMPLE,
    THREAD_REPLIES_RESPONSE_EXAMPLE,
    USER_BATCH_REQUEST_EXAMPLE,
    USER_BATCH_RESPONSE_EXAMPLE,
    USER_SEARCH_RESPONSE_EXAMPLE,
)
from apps.content.serializers import (
    ArticleDetailSerializer,
    ArticleEditorSerializer,
    ArticleSerializer,
    ArticleSubmitResponseSerializer,
    ArticleSummaryResponseSerializer,
    CommentCreateSerializer,
    CommentLikeSerializer,
    CommentLikeStatusSerializer,
    CommentResponseSerializer,
    ContributorOnboardingSerializer,
    CoverImageSerializer,
    ReviewActionRequestSerializer,
    ReviewActionResponseSerializer,
    ReviewStartResponseSerializer,
    TagSerializer,
    ThreadReplySerializer,
    UserBatchRequestSerializer,
    UserMentionSerializer,
    UserSearchRequestSerializer,
)
from apps.content.services import comment_like_service
from apps.content.services.ai_service import groq_service
from apps.content.throttles import (
    ArticleSummaryRegenerateThrottle,
    ArticleSummaryThrottle,
)
from apps.content.utils import (
    assign_reviewer,
    create_workflow_history,
    get_liveblocks_permissions,
    sync_content_from_liveblocks,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from django.db.models import Prefetch, Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
)
from redis import RedisError
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

article_tags = ["Articles"]
onboarding_tags = ["Onboarding"]
liveblock_tags = ["Liveblocks Integration"]
article_workflow = ["Article Workflow"]

logger = logging.getLogger(__name__)
security_logger = logging.getLogger("security")
User = get_user_model()


class AcceptGuidelinesView(APIView):
    """
    Accept contributor guidelines and become a contributor.

    Processes guideline acceptance and assigns contributor role to the user.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ContributorOnboardingSerializer

    @extend_schema(
        summary="Accept contributor guidelines",
        description="Accept contributor guidelines and terms to become a contributor. "
        "This endpoint processes acceptance, and assigns contributor role.",
        tags=onboarding_tags,
        responses=ACCEPT_GUIDELINES_RESPONSE_EXAMPLE,
    )
    def post(self, request):
        if request.user.groups.filter(name=UserRoles.CONTRIBUTOR).exists():
            return CustomResponse.success(message="Already a contributor")

        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            serializer.save()

            contributor_group, _ = Group.objects.get_or_create(
                name=UserRoles.CONTRIBUTOR
            )
            request.user.groups.add(contributor_group)
            logger.info(f"User {request.user.id} became contributor")

        return CustomResponse.success(
            message="Congratulations! You are now a Tech Hive contributor!",
            status_code=status.HTTP_201_CREATED,
        )


class ArticleListView(ListAPIView):
    # List all published article
    queryset = Article.published.select_related("category", "author").all()
    serializer_class = ArticleSerializer
    # serializer_class = ArticleCommentWithLikesSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("is_featured",)
    search_fields = ["title", "content"]
    pagination_class = DefaultPagination

    @extend_schema(
        summary="Retrieve a list of all published articles",
        description="This endpoint allows.",
        parameters=[
            OpenApiParameter(
                name="search",
                description="Search across title, and description.",
            ),
        ],
        tags=article_tags,
        auth=[],
        responses=ARTICLE_LIST_RESPONSE_EXAMPLE,
    )
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve profiles with pagination, search, and filtering.
        """
        return super().get(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data)
            return CustomResponse.success(
                message="Articles retrieved successfully.",
                data=paginated_data.data,
                status_code=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message="Articles retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class ArticleRetrieveView(APIView):
    serializer_class = ArticleDetailSerializer

    @extend_schema(
        summary="Retrieve article details",
        description="Retrieve detailed information about a specific article using the author's username and article slug.",
        tags=article_tags,
        responses=ARTICLE_DETAIL_RESPONSE_EXAMPLE,
    )
    def get(self, *args, **kwargs):
        try:
            article = (
                Article.published.prefetch_related(
                    Prefetch(
                        "comments",
                        queryset=Comment.objects.filter(is_active=True),
                    )
                )
                .select_related("author")
                .get(author__username=kwargs["username"], slug=kwargs["slug"])
            )

            serializer = self.serializer_class(article)
            return CustomResponse.success(
                message="Article detail retrieved successfully.",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
            )

        except Article.DoesNotExist:
            raise NotFoundError(err_msg="Article not found.")


class ThreadRepliesView(APIView):
    """View for fetching all replies in a thread"""

    serializer_class = ThreadReplySerializer

    @extend_schema(
        summary="Get replies for a thread",
        description=(
            "Retrieve all replies in a thread. Pass the root comment ID to get all replies. "
            "Returns replies sorted chronologically (oldest first) for natural conversation flow. "
            "Only works for root comments - returns error if called on a reply."
        ),
        tags=article_tags,
        responses=THREAD_REPLIES_RESPONSE_EXAMPLE,
    )
    def get(self, request, comment_id):
        """
        Get all replies in a thread.

        Args:
            comment_id: UUID of the ROOT comment (not a reply)
        """
        try:
            comment = Comment.active.select_related("thread", "user").get(
                id=comment_id,
            )
        except Comment.DoesNotExist:
            raise NotFoundError(err_msg="Comment not found")

        if not comment.is_root_comment:
            return CustomResponse.error(
                message="Can only fetch replies for root comments",
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                err_code=ErrorCode.VALIDATION_ERROR,
            )

        replies = (
            Comment.active.filter(
                thread=comment.thread,
            )
            .exclude(id=comment.id)  # Don't include root in replies list
            .select_related("user")
            .order_by("created_at")
        )  # Oldest first

        serializer = self.serializer_class(replies, many=True)

        return CustomResponse.success(
            message="Replies retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class CommentCreateView(APIView):
    """Create a new comment (root) or reply to existing thread"""

    permission_classes = [IsAuthenticated]
    serializer_class = CommentCreateSerializer

    @extend_schema(
        summary="Create a comment or reply",
        description=(
            "Create a new root comment on an article OR add a reply to an existing thread. "
            "If thread_id is provided, creates a reply. Otherwise, creates a new root comment. "
            "Threads are limited to 100 replies maximum."
        ),
        tags=article_tags,
        responses=COMMENT_CREATE_RESPONSE_EXAMPLE,
    )
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        comment = serializer.save()

        response_serializer = CommentResponseSerializer(comment)

        return CustomResponse.success(
            message="Comment created successfully.",
            data=response_serializer.data,
            status_code=status.HTTP_201_CREATED,
        )


class TagGenericView(ListAPIView):
    serializer_class = TagSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ["name"]
    queryset = Tag.objects.all()
    default_limit = 10  # TODO: TEST THIS TO MAKE SURE IT DOESN'T QUERY THE WHOLE DB

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        try:
            limit = int(request.query_params.get("limit", self.default_limit))
            if limit <= 0:
                limit = self.default_limit
        except ValueError:
            # if an invalid integer uses the default instead of crashing
            limit = self.default_limit

        queryset = queryset[:limit]

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data)
            return CustomResponse.success(
                message="Tags retrieved successfully.",
                data=paginated_data.data,
                status_code=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message="Tags retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="List all tags",
        description="Retrieve a list of all tags. Tags are keywords or labels that help categorize and organize articles, making it easier for users to find content related to specific topics.",
        tags=article_tags,
        responses=TAG_RESPONSE_EXAMPLE,
        auth=[],
        parameters=[
            OpenApiParameter(
                name="limit",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Maximum number of tags to return (default is 10).",
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RSSFeedInfoView(APIView):
    @extend_schema(
        summary="RSS Feed Information",
        description="Get information about subscribing to Tech Hive's RSS feed.",
        tags=article_tags,
        responses=RSS_RESPONSE_EXAMPLE,
    )
    def get(self, request):
        base_url = request.build_absolute_uri("/").rstrip("/")
        return CustomResponse.success(
            message="RSS Feed information retrieved successfully.",
            data={
                "rss_url": f"{base_url}/api/v1/articles/feed/",
                "description": "Subscribe to get the latest Tech Hive articles",
                "format": "RSS 2.0 XML",
                "items_count": 10,
                "update_frequency": "When new articles are published",
            },
            status_code=status.HTTP_200_OK,
        )


class CommentDeleteView(APIView):
    permission_classes = (IsAuthenticated, IsCommentAuthor)

    @extend_schema(
        summary="Delete a comment",
        description="Deletes a specific comment. Only the author of the comment can perform this action.",
        tags=article_tags,
        responses={204: None},
    )
    def delete(self, request, *args, **kwargs):
        comment_id = self.kwargs.get("comment_id")
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            raise NotFoundError("Comment not found.")

        self.check_object_permissions(request, comment)

        comment.delete()

        return CustomResponse.success(
            message="Comment deleted successfully.",
            status_code=status.HTTP_204_NO_CONTENT,
        )


class CommentLikeToggleView(APIView):
    """
    Toggle like status for a comment.
    If already liked, it will unlike. If not liked, it will like.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = CommentLikeSerializer

    @extend_schema(
        summary="Like or Unlike a Comment",
        description="Toggles the like status for a specific comment. If the user has already liked the comment, it will be unliked. If they haven't, it will be liked. This endpoint returns the new like status, the total like count, and the action performed ('liked' or 'unliked').",
        tags=article_tags,
        responses=COMMENT_LIKE_TOGGLE_RESPONSE_EXAMPLE,
    )
    def post(self, request, comment_id):
        """
        Toggle like on a comment.

        Args:
            comment_id: ID of the comment (from URL)

        Returns:
            200: Success with like status
            422: Unprocessible entity
            404: Comment not found
            503: Redis service unavailable
        """
        try:

            comment = Comment.active.select_related("user").get(id=comment_id)

            user_id = request.user.id

            try:
                result = comment_like_service.toggle_like(
                    comment_id=comment.id, user_id=user_id
                )
            except RedisError as e:
                logger.error(f"Redis error in toggle like: {e}")
                return CustomResponse.error(
                    message="Like service temporarily unavailable",
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    err_code=ErrorCode.SERVICE_UNAVAILABLE,
                )

            response_data = {
                "comment_id": comment.id,
                "is_liked": result["is_liked"],
                "like_count": result["like_count"],
            }
            message = (f"Comment {result['action']} successfully",)

            serializer = self.serializer_class(response_data)
            return CustomResponse.success(
                message=message, data=serializer.data, status_code=status.HTTP_200_OK
            )

        except Comment.DoesNotExist:
            raise NotFoundError("Comment not found")


class CommentLikeStatusView(APIView):
    """

    Get like status for a comment.
    """

    serializer_class = CommentLikeStatusSerializer

    @extend_schema(
        summary="Get Like Status for a Comment",
        description="Retrieves the total like count for a comment and indicates whether the current authenticated user has liked it. For unauthenticated users, `is_liked` will be `null`.",
        tags=article_tags,
        responses=COMMENT_LIKE_STATUS_RESPONSE_EXAMPLE,
    )
    def get(self, request, comment_id):
        """
        Get like status for a comment.

        Args:
            comment_id: ID of the comment (from URL)

        Returns:
            200: Success with like status
            404: Comment not found
            503: Redis service unavailable
        """
        try:

            comment = Comment.active.get(id=comment_id)

            user_id = request.user.id if request.user.is_authenticated else None

            try:
                result = comment_like_service.get_like_status(
                    comment_id=comment.id, user_id=user_id
                )
            except RedisError as e:
                logger.error(f"Redis error in get like status: {e}")
                return CustomResponse.error(
                    message="Like service temporarily unavailable",
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    err_code=ErrorCode.SERVICE_UNAVAILABLE,
                )

            response_data = {
                "comment_id": comment.id,
                "like_count": result["like_count"],
                "is_liked": result["is_liked"],
            }

            serializer = self.serializer_class(response_data)
            return CustomResponse.success(
                message="Comment like status retrieved successfully.",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
            )

        except Comment.DoesNotExist:
            raise NotFoundError("Comment not found")


class ArticleSummaryView(APIView):
    """
    Generate AI-powered bullet-point summary of an article using GROQ AI.

    This endpoint uses GROQ AI to generate a concise bullet-point summary
    of the article. Summaries are cached for 30 days for improved performance.

    Requirements:
    - User must be authenticated
    - Article must be published

    Query Parameters:
    - force_regenerate: Set to 'true' to bypass cache and generate a fresh summary
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleSummaryResponseSerializer
    throttle_classes = [ArticleSummaryThrottle, ArticleSummaryRegenerateThrottle]

    @extend_schema(
        summary="Generate AI Summary",
        description="Generate an AI-powered bullet-point summary of the article using GROQ AI. "
        "Summaries are cached for 30 days. Only published articles can be summarized.",
        responses=ARTICLE_SUMMARY_RESPONSE_EXAMPLE,
        tags=["Articles"],
        parameters=[
            OpenApiParameter(
                name="force_regenerate",
                type=str,
                location=OpenApiParameter.QUERY,
                # required=False,
                description="Set to true to bypass cache and generate a fresh summary",
            )
        ],
    )
    def post(self, request, article_id):
        """
        Generate AI summary for an article

        Args:
            article_id: UUID of the article to summarize

        Returns:
            Response with summary data or error message
        """
        force_regenerate = (
            request.query_params.get("force_regenerate", "false").lower() == "true"
        )

        try:
            article = Article.objects.get(id=article_id)

            if article.status != ArticleStatusChoices.PUBLISHED:
                return CustomResponse.error(
                    message="Cannot summarize unpublished articles",
                    err_code=ErrorCode.FORBIDDEN,
                    status_code=status.HTTP_403_FORBIDDEN,
                )

            if len(article.content.strip()) < 100:
                print(len(article.content.strip()))
                return CustomResponse.error(
                    message="Article content is too short to summarize",
                    err_code=ErrorCode.VALIDATION_ERROR,
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

            try:
                summary_data = groq_service.generate_summary(
                    article_id=str(article.id),
                    title=article.title,
                    content=article.content,
                    force_regenerate=force_regenerate,
                )

                response_data = {
                    "article_id": str(article.id),
                    "article_title": article.title,
                    "article_slug": article.slug,
                    "summary": summary_data["summary"],
                    "cached": summary_data["cached"],
                }

                if summary_data["cached"]:
                    message = "Article summary retrieved from cache."
                else:
                    message = "Article summary generated successfully."

                logger.info(
                    f"Summary {'regenerated' if force_regenerate else 'retrieved from cache' if summary_data['cached'] else 'generated'} "
                    f"for article {article.id} by user {request.user.id}"
                )

                return CustomResponse.success(
                    message,
                    response_data,
                    status_code=status.HTTP_200_OK,
                )

            except ValueError as e:
                logger.warning(
                    f"Content validation error for article {article.id}: {str(e)}"
                )
                return CustomResponse.error(
                    message=str(e),
                    err_code=ErrorCode.VALIDATION_ERROR,
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

            except Exception as e:
                logger.error(
                    f"AI service error for article {article.id}: {str(e)}",
                    exc_info=True,
                )
                return CustomResponse.error(
                    message="Summary generation service temporarily unavailable",
                    err_code=ErrorCode.VALIDATION_ERROR,
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

        except Article.DoesNotExist:
            logger.warning(f"Article not found: {article_id}")
            return CustomResponse.error(
                message="Article not found",
                err_code=ErrorCode.NON_EXISTENT,
                status_code=status.HTTP_404_NOT_FOUND,
            )

        # except Exception as e:
        #     logger.error(
        #         f"Unexpected error in article summary endpoint: {str(e)}", exc_info=True
        #     )
        #     return CustomResponse.error(
        #         message="An unexpected error occurred",
        #         err_code=ErrorCode.SERVER_ERROR,
        #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #     )


# ==========LIVEBLOCKS===============


class UserSearchView(APIView):
    """
    Search users for Liveblocks @mention suggestions.
    Results are filtered based on article access permissions.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserMentionSerializer

    @extend_schema(
        summary="Search users for mentions",
        description="""
        Search users by name or email for @mention suggestions in Liveblocks comments.
        Results are filtered based on the article's current status to ensure users
        can only mention people who have access to the article.
        
        Access rules:
        - Draft/Changes Requested: No comments shown (empty results)
        - Submitted/Under Review: Author + Assigned Reviewer
        - Ready for Publishing: Author + Assigned Reviewer + Assigned Editor
        - Published: Empty (comments disabled)
        """,
        parameters=[
            OpenApiParameter(
                name="q",
                type=str,
                location=OpenApiParameter.QUERY,
                required=True,
                description="Search query (min 1 character)",
                examples=[
                    OpenApiExample("Search by first name", value="john"),
                    OpenApiExample("Search by last name", value="doe"),
                    OpenApiExample("Partial search", value="jo"),
                ],
            ),
            OpenApiParameter(
                name="room_id",
                type=str,
                location=OpenApiParameter.QUERY,
                required=True,
                description="Liveblocks room ID",
                examples=[
                    OpenApiExample("Article room", value="article-123"),
                ],
            ),
        ],
        responses=USER_SEARCH_RESPONSE_EXAMPLE,
        tags=liveblock_tags,
    )
    def get(self, request):
        """Search users for @mention suggestions"""
        serializer = UserSearchRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        query = serializer.validated_data["q"].strip().lower()
        room_id = serializer.validated_data["room_id"]

        try:
            # Extract article ID and validate UUID format
            article_id_str = room_id.replace("article-", "")

            # Explicitly validate UUID format
            from uuid import UUID

            try:
                article_id = UUID(article_id_str)
            except ValueError:
                return CustomResponse.error(
                    message="Invalid article ID format. Expected a valid UUID.",
                    err_code=ErrorCode.VALIDATION_ERROR,
                )

            # Fetch article
            article = Article.objects.select_related(
                "author", "assigned_reviewer", "assigned_editor"
            ).get(id=article_id)

        except Article.DoesNotExist:
            raise NotFoundError()

        # Determine allowed users based on article status
        allowed_user_ids = self._get_allowed_users(article)

        # If no users allowed, return empty
        if not allowed_user_ids:
            return CustomResponse.success(
                message="No users available for mentions in this article status",  # ✅ Added
                data=[],
            )

        # Search users
        users = (
            User.objects.filter(id__in=allowed_user_ids, is_active=True)
            .filter(
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(email__icontains=query)
            )
            .select_related("profile")[:10]
        )  # Limit to 10 results

        serializer = self.serializer_class(users, many=True)
        return CustomResponse.success(
            message=(
                "Users retrieved successfully"
                if users
                else "No users found matching your search"
            ),
            data=serializer.data,
        )

    def _get_allowed_users(self, article):
        """
        Get list of user IDs who have access to the article
        based on current status
        """
        allowed_users = []

        if article.status in [
            ArticleStatusChoices.CHANGES_REQUESTED,
            ArticleStatusChoices.REJECTED,
        ]:
            if article.author:
                allowed_users.append(article.author.id)
            if article.assigned_reviewer:
                allowed_users.append(article.assigned_reviewer.id)

        # Comments not shown in UI
        else:
            return []

        # Remove duplicates and None values
        return list(set(filter(None, allowed_users)))


class UserBatchView(APIView):
    """
    Batch fetch user information for Liveblocks.
    Used to display user names, avatars, and colors in the UI.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserMentionSerializer

    @extend_schema(
        summary="Batch fetch user information",
        description="""
        Fetch information for multiple users by their IDs.
        Used by Liveblocks to display user names, avatars, and cursor colors
        in the editor UI, comments, and presence indicators.
        """,
        request=UserBatchRequestSerializer,
        responses=USER_BATCH_RESPONSE_EXAMPLE,
        examples=USER_BATCH_REQUEST_EXAMPLE,
        tags=liveblock_tags,
    )
    def post(self, request):
        """Batch fetch user information"""
        serializer = UserBatchRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_ids = serializer.validated_data["user_ids"]

        try:
            users = User.objects.filter(id__in=user_ids, is_active=True).select_related(
                "profile"
            )

            serializer = self.serializer_class(users, many=True)
            return CustomResponse.success("Users fetched", serializer.data)

        except Exception as e:
            logger.error(f"Error fetching users in batch: {str(e)}")
            return CustomResponse.error(
                message="Failed to fetch users",
                err_code=ErrorCode.SERVER_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ArticleCoverImageUploadView(APIView):
    """
    Upload or update cover image for an article.
    Only the author can upload cover images for their drafts.
    """

    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = CoverImageSerializer

    @extend_schema(
        summary="Upload article cover image",
        description="""
        Upload or update the cover image for an article.
        
        **Requirements:**
        - User must be the article author
        - Article must be in DRAFT, CHANGES_REQUESTED or REJECTED status
        - Image must be under 2MB
        - Supported formats: JPG, PNG, WEBP
        """,
        request={
            "multipart/form-data": CoverImageSerializer,
        },
        responses=COVER_IMAGE_RESPONSE_EXAMPLE,
        tags=article_tags,
    )
    def patch(self, request, article_id):
        """Upload cover image for an article"""
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            raise NotFoundError("Article not found")

        self.check_object_permissions(request, article)

        # Check article status
        if article.status not in [
            ArticleStatusChoices.DRAFT,
            ArticleStatusChoices.CHANGES_REQUESTED,
            ArticleStatusChoices.REJECTED,
        ]:
            return CustomResponse.error(
                message="Can only upload cover images for draft or rejected or articles with requested changes",
                err_code=ErrorCode.VALIDATION_ERROR,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        serializer = self.serializer_class(article, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        article = serializer.save()

        return CustomResponse.success(
            message="Cover image uploaded successfully",
            data={"cover_image_url": article.cover_image_url},
        )


class ArticleEditorView(APIView):
    """
    Load article data for Liveblocks editor.
    Returns article content and metadata with appropriate permissions.
    """

    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = ArticleEditorSerializer

    @extend_schema(
        summary="Load article for editor",
        description="""
        Fetch article data for the Liveblocks collaborative editor.
        
        **Access Rules:**
        - Draft/Changes Requested: Only author can access
        - Submitted/Under Review/Rejected: Author (read) + Assigned Reviewer (write)
        - Ready for Publishing: Author/Reviewer (read) + Assigned Editor (write)
        - Published: Author can view (read-only), others redirected
        
        
        **Returns:**
        - Complete article data
        - Liveblocks room ID
        - Edit permissions for current user
        - User info for all assigned roles
        """,
        responses=ARTICLE_EDITOR_RESPONSE_EXAMPLE,
        examples=ARTICLE_EDITOR_EXAMPLE,
        tags=liveblock_tags,
    )
    def get(self, request, article_id):
        """Load article for Liveblocks editor"""
        try:
            article = (
                Article.objects.select_related(
                    "author", "assigned_reviewer", "assigned_editor", "category"
                )
                .prefetch_related("tags")
                .get(id=id)
            )
        except Article.DoesNotExist:
            raise NotFoundError("Article not found")
        
        self.check_object_permissions(request, article)

        user = request.user
        permission_level = get_liveblocks_permissions(user, article)

        # NO ACCESS - Forbidden
        if permission_level == "NONE":
            return CustomResponse.error(
                message="You don't have permission to access this article",
                err_code=ErrorCode.FORBIDDEN,
                status_code=status.HTTP_403_FORBIDDEN,
            )

        # PUBLISHED - Special handling
        if article.status == ArticleStatusChoices.PUBLISHED:
            # If user is the author, allow read-only access
            if user == article.author:
                serializer = self.serializer_class(
                    article, context={"request": request}
                )
                return CustomResponse.info(
                    message="Article is published. Read-only mode.",
                    data=serializer.data,
                )
            else:
                # Redirect others to public view
                redirect_url = f"/articles/{article.author.username}/{article.slug}"
                return CustomResponse.info(
                    message="Article is published. Redirecting to public view.",
                    data={"redirect_url": redirect_url},
                )

        # Return article data (WRITE or READ access)
        serializer = self.serializer_class(article, context={"request": request})

        return CustomResponse.success(
            message="Article loaded successfully",
            data=serializer.data,
        )


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
        tags=article_workflow,
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
        tags=article_workflow,
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
        tags=article_workflow,
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
                    "reviewer_notes", ""
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


# TODO:
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