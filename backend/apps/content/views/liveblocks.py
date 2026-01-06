import logging

from apps.common.errors import ErrorCode
from apps.common.exceptions import NotFoundError
from apps.common.responses import CustomResponse
from apps.content.choices import ArticleStatusChoices
from apps.content.models import Article
from apps.content.permissions import IsAuthorOrReadOnly
from apps.content.schema_examples import (
    ARTICLE_EDITOR_EXAMPLE,
    ARTICLE_EDITOR_RESPONSE_EXAMPLE,
    USER_BATCH_REQUEST_EXAMPLE,
    USER_BATCH_RESPONSE_EXAMPLE,
    USER_SEARCH_RESPONSE_EXAMPLE,
)
from apps.content.serializers import (
    ArticleEditorSerializer,
    LiveblocksAuthRequestSerializer,
    UserBatchRequestSerializer,
    UserMentionSerializer,
    UserSearchRequestSerializer,
)
from apps.content.utils import create_liveblocks_token, get_liveblocks_permissions
from django.contrib.auth import get_user_model
from django.db.models import Q
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

tags = ["Liveblocks Integration"]

logger = logging.getLogger(__name__)

User = get_user_model()


class LiveblocksAuthView(APIView):
    """
    Authenticate users for Liveblocks room access.

    This endpoint implements the authentication logic required by Liveblocks.
    It generates JWT tokens with appropriate room permissions based on the
    article's workflow state and the user's role.

    Documentation: https://liveblocks.io/docs/authentication/access-token
    """

    permission_classes = [IsAuthenticated]
    serializer_class = None

    @extend_schema(
        summary="Authenticate for Liveblocks room",
        description="""
        Generate a JWT token for Liveblocks room access.
        
        **How it works:**
        1. Client (React) calls this endpoint with a room ID
        2. Server validates user's access to the article
        3. Server generates JWT with appropriate permissions:
           - WRITE: `["room:write"]` - Full editing access
           - READ: `["room:read", "room:presence:write"]` - Read-only with comments
           - NONE: Access denied
        
        **Access Rules:**
        - Draft/Changes Requested: Only author has WRITE access
        - Submitted/Under Review: Assigned reviewer has WRITE, author has READ
        - Ready for Publishing: Assigned editor has WRITE, author/reviewer have READ
        - Published: Everyone has READ access
        - Rejected: No access (except author for viewing from article list)
        
        **Token includes:**
        - User ID
        - User info (name, avatar, cursor color)
        - Room permissions
        - Expiration (2 hours)
        """,
        # request=LiveblocksAuthRequestSerializer,
        # responses={
        #     200: LiveblocksAuthResponseSerializer,
        #     400: OpenApiExample(
        #         'Invalid Request',
        #         value={
        #             "status": "failure",
        #             "message": "Invalid room format",
        #             "code": "invalid_input"
        #         }
        #     ),
        #     403: OpenApiExample(
        #         'Access Denied',
        #         value={
        #             "status": "failure",
        #             "message": "You don't have permission to access this room",
        #             "code": "forbidden"
        #         }
        #     ),
        #     404: OpenApiExample(
        #         'Article Not Found',
        #         value={
        #             "status": "failure",
        #             "message": "Article not found",
        #             "code": "non_existent"
        #         }
        #     ),
        #     500: OpenApiExample(
        #         'Token Generation Failed',
        #         value={
        #             "status": "failure",
        #             "message": "Failed to generate authentication token",
        #             "code": "server_error"
        #         }
        #     )
        # },
        # examples=[
        #     OpenApiExample(
        #         'Request Example',
        #         value={"room": "article-123"},
        #         request_only=True
        #     ),
        #     OpenApiExample(
        #         'Success Response - Write Access',
        #         value={
        #             "status": "success",
        #             "message": "Authentication successful",
        #             "data": {
        #                 "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        #                 "userId": "5"
        #             }
        #         },
        #         response_only=True
        #     ),
        #     OpenApiExample(
        #         'Success Response - Read Access',
        #         value={
        #             "status": "success",
        #             "message": "Authentication successful (read-only)",
        #             "data": {
        #                 "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        #                 "userId": "5"
        #             }
        #         },
        #         response_only=True
        #     )
        # ],
        tags=tags,
    )
    def post(self, request):
        """Generate Liveblocks authentication token"""

        serializer = LiveblocksAuthRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room_id = serializer.validated_data["room_id"]

        # Extract article ID from room ID
        try:
            article_id = room_id.replace("article-", "")
            article = Article.objects.select_related(
                "author", "assigned_reviewer", "assigned_editor"
            ).get(id=article_id)
        except (ValueError, Article.DoesNotExist):
            logger.warning(
                f"Liveblocks auth failed: Article not found for room {room_id}",
                extra={"user_id": request.user.id, "room_id": room_id},
            )
            return CustomResponse.error(
                message="Article not found",
                err_code=ErrorCode.UNPROCESSABLE_ENTITY,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        user = request.user
        permission_level = get_liveblocks_permissions(user, article)

        if permission_level == "NONE":
            logger.warning(
                f"Liveblocks auth denied: User {user.id} has no access to article {article.id}",
                extra={
                    "user_id": user.id,
                    "article_id": article.id,
                    "article_status": article.status,
                },
            )
            return CustomResponse.error(
                message="You don't have permission to access this room",
                err_code=ErrorCode.FORBIDDEN,
                status_code=status.HTTP_403_FORBIDDEN,
            )

        try:
            token = create_liveblocks_token(user, article, permission_level)

            logger.info(
                f"Liveblocks auth successful: User {user.id} granted {permission_level} access to article {article.id}",
                extra={
                    "user_id": user.id,
                    "article_id": article.id,
                    "permission_level": permission_level,
                },
            )

            response_data = {"token": token, "user_id": str(user.id)}

            message = "Authentication successful"
            if permission_level == "READ":
                message = "Authentication successful (read-only)"

            return CustomResponse.success(
                message=message, data=response_data, status_code=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(
                f"Failed to generate Liveblocks token for user {user.id}: {str(e)}",
                extra={"user_id": user.id, "article_id": article.id},
                exc_info=True,
            )
            return CustomResponse.error(
                message="Failed to generate authentication token",
                err_code=ErrorCode.SERVER_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
        tags=tags,
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
        tags=tags,
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
        tags=tags,
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
