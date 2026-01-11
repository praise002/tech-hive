import logging

from apps.common.errors import ErrorCode
from apps.common.exceptions import NotFoundError
from apps.common.responses import CustomResponse
from apps.content.choices import ArticleStatusChoices
from apps.content.models import Article, ArticleReaction
from apps.content.schema_examples import (
    ARTICLE_REACTION_STATUS_RESPONSE_EXAMPLE,
    ARTICLE_REACTION_TOGGLE_RESPONSE_EXAMPLE,
)
from apps.content.serializers import (
    ArticleReactionStatusSerializer,
    ArticleReactionToggleSerializer,
)
from apps.notification.utils import create_notification
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

tags = ["Articles"]


class ArticleReactionView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ArticleReactionToggleSerializer
        return ArticleReactionStatusSerializer

    def get_serializer(self, *args, **kwargs):
        """
        Helper to get an instance of the correct serializer.
        """
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    @extend_schema(
        summary="Get reaction status for an article",
        description="Retrieve the reaction statistics for a published article, including the count for each emoji type and the total reaction count. If the user is authenticated, it also returns which reactions the user has added.",
        tags=tags,
        responses=ARTICLE_REACTION_STATUS_RESPONSE_EXAMPLE,
    )
    def get(self, request, article_id):
        """
        Get reaction status for an article.

        Args:
            article_id: ID of the article (from URL)

        Returns:
            200: Success with reaction status
            404: Article not found
            500: Server error
        """
        try:

            article = (
                Article.published.select_related("author", "category")
                .prefetch_related("tags", "reactions")
                .get(id=article_id)
            )

            reaction_counts = article.reaction_counts
            total_reactions = article.total_reaction_counts

            user_reactions = None
            if request.user.is_authenticated:
                user_reactions = list(
                    ArticleReaction.objects.filter(
                        user=request.user, article=article
                    ).values_list("reaction_type", flat=True)
                )

            response_data = {
                "article_id": article.id,
                "reaction_counts": reaction_counts,
                "total_reactions": total_reactions,
                "user_reactions": user_reactions,
            }

            serializer = self.get_serializer(response_data)
            return CustomResponse.success(
                message="Reaction status retrieved successfully",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
            )

        except Article.DoesNotExist:
            raise NotFoundError(err_msg="Article not found")

    @extend_schema(
        summary="Toggle reaction on an article",
        description="Add or remove a reaction (emoji) on a published article. If the user has already reacted with the specified emoji, it will be removed. If not, it will be added. Users can have multiple different reactions on the same article.",
        tags=tags,
        responses=ARTICLE_REACTION_TOGGLE_RESPONSE_EXAMPLE,
    )
    def post(self, request, article_id):
        """
        Toggle reaction on an article.

        Args:
            article_id: ID of the article (from URL)

        Request body:
            {
                "reaction_type": "❤️"  // One of: ❤️, 😍, 👍, 🔥
            }

        Returns:
            200: Success with updated reaction status
            422: Invalid reaction type or bad request
            401: Not authenticated
            403: Article not published
            404: Article not found
            500: Server error
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            reaction_type = serializer.validated_data["reaction_type"]

            article = Article.objects.select_related("author", "category").get(
                id=article_id
            )

            if article.status != ArticleStatusChoices.PUBLISHED:
                return CustomResponse.error(
                    message="Cannot react to unpublished articles",
                    err_code=ErrorCode.FORBIDDEN,
                    status_code=status.HTTP_403_FORBIDDEN,
                )

            user = request.user

            existing_reaction = ArticleReaction.objects.filter(
                user=user, article=article, reaction_type=reaction_type
            ).first()

            if existing_reaction:
                # User already reacted with this emoji - REMOVE IT
                existing_reaction.delete()
                action = "removed"
                is_reacted = False
                logger.info(
                    f"User {user.id} {action} {reaction_type} from article {article.id}"
                )
            else:
                # User hasn't reacted with this emoji - ADD IT
                ArticleReaction.objects.create(
                    user=user, article=article, reaction_type=reaction_type
                )
                action = "added"
                is_reacted = True
                logger.info(
                    f"User {user.id} {action} {reaction_type} to article {article.id}"
                )

                # Create notification for article author (only when adding reaction)
                if article.author != user:
                    verb = f"{reaction_type} your article '{article.title}'"
                    create_notification(
                        recipient=article.author, verb=verb, target=article, actor=user
                    )

            reaction_counts = article.reaction_counts
            total_reactions = article.total_reaction_counts

            response_data = {
                "article_id": article.id,
                "reaction_type": reaction_type,
                "action": action,
                "is_reacted": is_reacted,
                "reaction_counts": reaction_counts,
                "total_reactions": total_reactions,
            }
            message = f"Reaction {action} successfully"

            response_serializer = self.get_serializer(response_data)
            return CustomResponse.success(
                message=message,
                data=response_serializer.data,
                status_code=status.HTTP_200_OK,
            )

        except Article.DoesNotExist:
            raise NotFoundError(err_msg="Article not found")
