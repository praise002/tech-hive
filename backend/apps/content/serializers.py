from apps.accounts.models import ContributorOnboarding, User
from apps.content import models
from apps.content.choices import ArticleStatusChoices
from apps.content.models import (
    Article,
    ArticleReaction,
    ArticleReview,
    ArticleWorkflowHistory,
    Comment,
    CommentMention,
    CommentThread,
)
from apps.notification.utils import create_notification
from apps.profiles.serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.db.models import F
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

User = get_user_model()


def process_tags(tag_names):
    """Convert tag names to Tag instances using get_or_create"""
    tag_instances = []
    for tag_name in tag_names:
        cleaned_name = tag_name.strip().lower()
        if cleaned_name:  # Skip empty strings
            tag, _ = models.Tag.objects.get_or_create(name=cleaned_name)
            tag_instances.append(tag)
    return tag_instances


class ContributorOnboardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContributorOnboarding
        fields = ["terms_accepted"]

    def validate_terms_accepted(self, value):
        if not value:
            raise serializers.ValidationError(
                "You must accept the terms and conditions."
            )
        return value

    def create(self, validated_data):
        # Get the authenticated user's
        user = self.context["request"].user

        contributor = ContributorOnboarding.objects.create(user=user, **validated_data)

        return contributor


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ["id", "name"]


class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ["name"]
        extra_kwargs = {"name": {"validators": []}}  # Remove default unique validator

    def create(self, validated_data):
        tag, created = models.Tag.objects.get_or_create(
            name=validated_data["name"].lower()
        )
        return tag, created


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ["id", "name", "desc", "slug"]


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    cover_image_url = serializers.SerializerMethodField()
    read_time = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    total_reaction_counts = serializers.SerializerMethodField()
    reaction_counts = serializers.SerializerMethodField()

    class Meta:
        model = models.Article
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "cover_image_url",
            "read_time",
            "status",
            "created_at",
            "is_featured",
            "author",
            "total_reaction_counts",
            "reaction_counts",
            "tags",
        ]

    @extend_schema_field(serializers.URLField)
    def get_cover_image_url(self, obj):
        return obj.cover_image_url

    @extend_schema_field(serializers.IntegerField)
    def get_read_time(self, obj):
        return obj.calculate_read_time()

    @extend_schema_field(serializers.CharField)
    def get_author(self, obj):
        return obj.author.full_name

    @extend_schema_field(serializers.IntegerField)
    def get_total_reaction_counts(self, obj):
        return obj.total_reaction_counts

    @extend_schema_field(serializers.IntegerField)
    def get_reaction_counts(self, obj):
        return obj.reaction_counts


class ArticleCreateSerializer(serializers.ModelSerializer):
    # url = CustomHyperlinkedIdentityField(
    #     view_name="article_detail",
    #     lookup_fields=[
    #         (
    #             "author.username",
    #             "username",
    #         ),  # Get username from article.author.username
    #         ("slug", "slug"),  # Get slug from article.slug
    #     ],
    # )
    url = serializers.HyperlinkedIdentityField(
        view_name="article_detail", lookup_field="slug"
    )

    class Meta:
        model = models.Article
        fields = [
            "title",
            "content",
            "url",
        ]

    def create(self, validated_data):
        # Get the authenticated user's profile
        user = self.context["request"].user

        # Create the author and associate it with the user
        article = models.Article.objects.create(author=user, **validated_data)

        return article


class ArticleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = [
            "title",
            "cover_image",
        ]


class ArticleReactionSerializer(serializers.ModelSerializer):
    # For POST/PUT/PATCH
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())

    class Meta:
        model = models.ArticleReaction
        fields = ["id", "user", "article", "reaction_type"]


class SavedArticleSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()

    class Meta:
        model = models.SavedArticle
        fields = ["id", "article"]


class SaveArticleCreateSerializer(serializers.Serializer):
    """Serializer for saving/unsaving articles"""

    article_id = serializers.UUIDField()

    def validate_article_id(self, article_id):
        """Validate that the article exists and is published"""
        try:
            article = models.Article.objects.get(id=article_id)
        except models.Article.DoesNotExist:
            raise serializers.ValidationError("Article not found")

        self.article = article

        return article_id


class CommentSerializer(serializers.ModelSerializer):
    article_id = serializers.SerializerMethodField()
    article_title = serializers.CharField(source="article.title", read_only=True)
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = [
            "id",
            "user_id",
            "article_id",
            "article_title",
            "created_at",
            "body",
        ]

    @extend_schema_field(serializers.UUIDField)
    def get_article_id(self, obj):
        return str(obj.article.id)

    @extend_schema_field(serializers.UUIDField)
    def get_user_id(self, obj):
        return str(obj.user.id)


class CommentCreateSerializer(serializers.ModelSerializer):
    article_id = serializers.UUIDField(required=True)
    thread_id = serializers.UUIDField(required=False)

    class Meta:
        model = models.Comment
        fields = ["article_id", "thread_id", "body"]

    def validate(self, data):
        """Validate article and thread relationship"""

        # Validate article exists and is published
        try:
            article = (
                Article.objects.select_related("author", "category")
                .prefetch_related("tags")
                .get(id=data["article_id"])
            )
        except Article.DoesNotExist:
            raise serializers.ValidationError("Article not found")

        if article.status != ArticleStatusChoices.PUBLISHED:
            raise PermissionDenied("Cannot comment on unpublished articles")

        # If thread_id provided, validate it belongs to the article
        if data.get("thread_id"):
            try:
                thread = CommentThread.objects.select_related("root_comment").get(
                    id=data["thread_id"], article_id=data["article_id"], is_active=True
                )

                # Check thread hasn't reached max replies
                if thread.reply_count >= 100:
                    raise serializers.ValidationError(
                        "This thread has reached the maximum number of replies (100)"
                    )

                # Store thread for use in create()
                self.thread = thread

            except CommentThread.DoesNotExist:
                raise serializers.ValidationError("Thread not found")
        else:
            self.thread = None

        # Store article for use in create()
        self.article = article

        return data

    def create(self, validated_data):
        """Create root comment or reply with proper thread handling"""

        from django.db import transaction

        user = self.context["request"].user

        with transaction.atomic():
            if self.thread:
                # CASE: Creating a reply
                comment = Comment.objects.create(
                    article=self.article,
                    thread=self.thread,
                    user=user,
                    body=validated_data["body"],
                )

                # Increment thread reply count
                CommentThread.objects.filter(id=self.thread.id).update(
                    reply_count=F("reply_count") + 1
                )

                self.thread.refresh_from_db()

                # Notify the root comment author (thread starter) about the reply
                root_comment_author = self.thread.root_comment.user
                if (
                    root_comment_author != user
                ):  # Don't notify if replying to own thread
                    create_notification(
                        root_comment_author, "replied to your thread", comment, user
                    )

                # Notify post author
                recipient = self.article.author

                if recipient != user:
                    create_notification(
                        recipient, "commented on your post", comment, user
                    )

                # NOTE: The business logic is to only allow @mention inside a thread
                # So only a reply can mention
                mentions = self.extract_mentions(validated_data["body"])

                for username in mentions:
                    try:
                        recipient = User.objects.only(
                            "id", "username", "mentions_disabled"
                        ).get(username=username)
                        if self.can_be_mentioned(recipient, comment):
                            mention = CommentMention.objects.create(
                                comment=comment, mentioned_user=recipient
                            )
                            # 4. Create notification
                            create_notification(
                                recipient, "mentioned you in a comment", mention, user
                            )

                    except User.DoesNotExist:
                        pass

            else:
                # CASE: Creating root comment (new thread)
                # Step 1: Create comment without thread
                comment = Comment.objects.create(
                    article=self.article,
                    user=user,
                    body=validated_data["body"],
                )

                # Step 2: Create thread pointing to this comment
                thread = CommentThread.objects.create(
                    article=self.article,
                    root_comment=comment,
                )

                # Step 3: Link comment back to thread
                comment.thread = thread
                comment.save(update_fields=["thread"])

                recipient = self.article.author

                if recipient != user:  # Don't notify if commenting on own article
                    create_notification(
                        recipient, "commented on your post", comment, user
                    )

        return comment

    def extract_mentions(self, text):
        """Extract @mentions from text"""
        import re

        pattern = r"\B@([\w-]+)"
        matches = re.findall(pattern, text)
        return list(set(matches))

    def can_be_mentioned(self, user, comment):
        """Validate if user can be mentioned"""
        return not user.mentions_disabled and user != comment.user


class CommentResponseSerializer(serializers.ModelSerializer):
    """Serializer for returning comment data after creation"""

    user_name = serializers.CharField(source="user.full_name", read_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)
    user_avatar = serializers.URLField(source="user.avatar_url", read_only=True)
    thread_id = serializers.UUIDField(source="thread.id", read_only=True)
    is_root = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = [
            "id",
            "thread_id",
            "body",
            "created_at",
            "user_name",
            "user_username",
            "user_avatar",
            "is_root",
        ]

    @extend_schema_field(serializers.BooleanField)
    def get_is_root(self, obj):
        return obj.is_root_comment


class ArticleCommentSerializer(serializers.ModelSerializer):
    """Serializer for displaying comments on articles with lazy-loading support"""

    user_name = serializers.CharField(source="user.full_name", read_only=True)
    user_avatar = serializers.URLField(source="user.avatar_url", read_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)
    total_replies = serializers.SerializerMethodField()
    thread_id = serializers.UUIDField(source="thread.id", read_only=True)

    class Meta:
        model = models.Comment
        fields = [
            "id",
            "thread_id",
            "body",
            "created_at",
            "user_name",
            "user_username",
            "user_avatar",
            "total_replies",
        ]

    @extend_schema_field(serializers.IntegerField)
    def get_total_replies(self, obj):
        """Count active replies for this comment"""
        return obj.get_all_replies_count()


class ArticleDetailSerializer(ArticleSerializer):
    comments = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields + ["comments", "comments_count"]

    @extend_schema_field(ArticleCommentSerializer(many=True))
    def get_comments(self, obj):
        """Get root comments only (comments that start threads)"""
        root_comments = [
            comment
            for comment in obj.comments.all()
            if comment.thread is not None
            and comment.thread.root_comment_id == comment.id
        ]

        # Sort by recency (newest first) - TODO: CHECK IF IT SORTS BY DEFAULT
        root_comments.sort(key=lambda x: x.created_at, reverse=True)

        serializer = ArticleCommentSerializer(
            root_comments,
            many=True,
        )
        return serializer.data

    @extend_schema_field(serializers.IntegerField)
    def get_comments_count(self, obj):
        """Get total count of all active comments on article"""
        return obj.all_comments_count


class ThreadReplySerializer(serializers.ModelSerializer):
    """Serializer for displaying replies in a thread"""

    user_name = serializers.CharField(source="user.full_name", read_only=True)
    user_avatar = serializers.URLField(source="user.avatar_url", read_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = models.Comment
        fields = [
            "id",
            "body",
            "created_at",
            "user_name",
            "user_username",
            "user_avatar",
        ]


class JobSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = models.Job
        fields = [
            "id",
            "title",
            "company",
            "desc",
            "requirements",
            "responsibilities",
            "url",
            "salary",
            "location",
            "job_type",
            "work_mode",
            "category",
        ]


class EventSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = models.Event
        fields = [
            "id",
            "title",
            "desc",
            "start_date",
            "end_date",
            "location",
            "agenda",
            "ticket_url",
            "category",
        ]


class ResourceSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Resource
        fields = ["id", "name", "image_url", "body", "url", "category", "is_featured"]

    @extend_schema_field(serializers.CharField)
    def get_image_url(self, obj):
        return obj.image_url


class ToolTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ToolTag
        fields = ["id", "name"]


class ToolSerializer(serializers.ModelSerializer):
    tags = ToolTagSerializer(many=True, read_only=True)
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = models.Tool
        fields = [
            "id",
            "name",
            "desc",
            "url",
            "image_url",
            "call_to_action",
            "tags",
            "category",
            "is_featured",
        ]


class CommentLikeSerializer(serializers.Serializer):
    """
    Serializer for comment like response.
    """

    comment_id = serializers.UUIDField(read_only=True)
    is_liked = serializers.BooleanField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    message = serializers.CharField(read_only=True)


class CommentLikeStatusSerializer(serializers.Serializer):
    """
    Serializer for getting like status without modifying it.
    """

    comment_id = serializers.UUIDField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(
        read_only=True, allow_null=True
    )  # None for unauthenticated users


class ArticleCommentWithLikesSerializer(ArticleSerializer):
    """
    Extended comment serializer that includes like data.
    """

    like_count = serializers.IntegerField(read_only=True)
    is_liked_by_current_user = serializers.BooleanField(read_only=True)

    class Meta(ArticleSerializer.Meta):
        model = Comment
        fields = ArticleSerializer.Meta.fields + [
            "like_count",
            "is_liked_by_current_user",
        ]


class ArticleReactionToggleSerializer(serializers.Serializer):
    """
    Serializer for toggling article reactions.
    Input: reaction_type
    Output: reaction status and counts
    """

    # INPUT field
    reaction_type = serializers.ChoiceField(
        choices=ArticleReaction.EMOJI_CHOICES,
        required=True,
        help_text="The emoji reaction type",
    )

    # OUTPUT fields (read-only, returned in response)
    article_id = serializers.UUIDField(read_only=True)
    action = serializers.CharField(read_only=True)  # "added" or "removed"
    is_reacted = serializers.BooleanField(read_only=True)
    reaction_counts = serializers.DictField(read_only=True)
    total_reactions = serializers.IntegerField(read_only=True)


class ArticleReactionStatusSerializer(serializers.Serializer):
    """
    Serializer for getting article reaction status.
    Output only (no input fields).
    """

    article_id = serializers.UUIDField(read_only=True)
    reaction_counts = serializers.DictField(
        read_only=True, help_text="Dictionary of reaction types and their counts"
    )
    total_reactions = serializers.IntegerField(
        read_only=True, help_text="Total number of reactions across all types"
    )
    user_reactions = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
        allow_null=True,
        help_text="List of reaction types the current user has used (null if not authenticated or no reaction)",
    )


class UserMentionSerializer(serializers.ModelSerializer):
    """
    Serializer for user mention data in Liveblocks
    Used for both search results and batch lookup
    """

    name = serializers.CharField(read_only=True, source="full_name")
    # SerializerMethodField is read-only by default
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "name", "avatar_url", "cursor_color"]

    @extend_schema_field(serializers.CharField)
    def get_avatar_url(self, obj):
        return obj.avatar_url


class UserSearchRequestSerializer(serializers.Serializer):
    """Validate search query parameters"""

    q = serializers.CharField(
        required=True,
        min_length=1,
        max_length=100,
        help_text="Search query for user names or emails",
    )
    room_id = serializers.CharField(
        required=True, help_text="Liveblocks room ID (e.g., 'article-123')"
    )

    def validate_room_id(self, value):
        """Validate room_id format"""
        if not value.startswith("article-"):
            raise serializers.ValidationError(
                "Invalid room_id format. Expected format: 'article-{id}'"
            )
        return value


class UserBatchRequestSerializer(serializers.Serializer):
    """Validate batch user lookup request"""

    user_ids = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
        max_length=50,
        help_text="List of user IDs to fetch",
    )


class EditorUserSerializer(serializers.ModelSerializer):
    """Minimal user info for editor response"""

    name = serializers.CharField(source="full_name", read_only=True)
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "name", "avatar_url"]

    @extend_schema_field(serializers.URLField)
    def get_avatar_url(self, obj):
        return obj.avatar_url


class ArticleEditorSerializer(serializers.ModelSerializer):
    """
    Complete article data for Liveblocks editor.
    Includes all metadata needed for the editing interface.
    """

    liveblocks_room_id = serializers.SerializerMethodField()
    user_can_edit = serializers.SerializerMethodField()
    is_published = serializers.SerializerMethodField()

    author = EditorUserSerializer(read_only=True)
    assigned_reviewer = EditorUserSerializer(read_only=True)
    assigned_editor = EditorUserSerializer(read_only=True)

    category = CategorySerializer(read_only=True)

    tags = TagSerializer(many=True, read_only=True)
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Article
        fields = [
            "id",
            "category",  # will be available if it is published
            "title",
            "slug",
            "content",
            "cover_image_url",
            "status",
            "liveblocks_room_id",
            "user_can_edit",
            "is_published",
            "author",
            "assigned_reviewer",
            "assigned_editor",
            "tags",  # will be available if it is published
            "created_at",
            "content_last_synced_at",
            "updated_at",
        ]
        read_only_fields = fields

    @extend_schema_field(serializers.URLField)
    def get_cover_image_url(self, obj):
        return obj.cover_image_url

    @extend_schema_field(serializers.CharField)
    def get_liveblocks_room_id(self, obj):
        """Generate Liveblocks room ID"""
        return f"article-{obj.id}"

    @extend_schema_field(serializers.BooleanField)
    def get_user_can_edit(self, obj):
        """Determine if current user can edit"""
        request = self.context.get("request")
        if not request:
            return False

        user = request.user
        from apps.content.utils import get_liveblocks_permissions

        permission_level = get_liveblocks_permissions(user, obj)
        return permission_level == "WRITE"

    @extend_schema_field(serializers.BooleanField)
    def get_is_published(self, obj):
        """Check if article is published"""
        from apps.content.choices import ArticleStatusChoices

        return obj.status == ArticleStatusChoices.PUBLISHED


# class CoverImageSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = models.Article
#         fields = [
#             "cover_image",
#         ]


class ReviewActionRequestSerializer(serializers.Serializer):
    """Request body for review actions (request changes, approve, reject)"""

    reviewer_notes = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=5000,
        help_text="Private notes for reviewer's reference (not shown to author)",
    )


class WorkflowUserSerializer(serializers.ModelSerializer):
    """User info for workflow responses"""

    name = serializers.CharField(source="get_full_name", read_only=True)
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "name", "username", "avatar_url"]

    @extend_schema_field(serializers.URLField)
    def get_avatar_url(self, obj):
        return obj.avatar_url


# Response serializer
class ArticleSummaryResponseSerializer(serializers.Serializer):
    """Serializer for article summary response"""

    article_id = serializers.UUIDField(read_only=True)
    article_title = serializers.CharField(read_only=True)
    article_slug = serializers.CharField(read_only=True)
    summary = serializers.CharField(read_only=True)
    cached = serializers.BooleanField(read_only=True)


class ArticleSubmitResponseSerializer(serializers.Serializer):
    """Serializer for article submission response"""

    status = serializers.CharField(
        read_only=True, help_text="Article status after submission"
    )
    # assigned_reviewer = serializers.SerializerMethodField(
    #     help_text="Reviewer assigned to the article"
    # )
    # assigned_editor = serializers.SerializerMethodField(
    #     help_text="Editor assigned to the article"
    # )
    is_resubmission = serializers.BooleanField(
        read_only=True, help_text="Whether this is a resubmission to the same reviewer"
    )

    # @extend_schema_field(serializers.DictField)
    # def get_assigned_reviewer(self, obj):
    #     """Return reviewer info"""
    #     reviewer = obj.get("assigned_reviewer")
    #     if reviewer:
    #         return {
    #             "id": str(reviewer.id),
    #             "name": reviewer.full_name,
    #             "username": reviewer.username,
    #             "avatar_url": reviewer.avatar_url,
    #         }
    #     return None

    # @extend_schema_field(serializers.DictField)
    # def get_assigned_editor(self, obj):
    #     """Return editor info"""
    #     editor = obj.get("assigned_editor")
    #     if editor:
    #         return {
    #             "id": str(editor.id),
    #             "name": editor.full_name,
    #             "username": editor.username,
    #             "avatar_url": editor.avatar_url,
    #         }
    #     return None


class ReviewStartResponseSerializer(serializers.Serializer):
    """Response for starting review"""

    review_status = serializers.CharField(
        read_only=True, help_text="Review status (e.g., 'in_progress')"
    )
    article_status = serializers.CharField(
        read_only=True, help_text="Article status (e.g., 'under_review')"
    )
    started_at = serializers.DateTimeField(
        read_only=True, help_text="Timestamp when review was started"
    )


class ReviewActionResponseSerializer(serializers.Serializer):
    """Response for review actions (request changes, reject)"""

    article_status = serializers.CharField(
        read_only=True, help_text="Article status after action"
    )
    completed_at = serializers.DateTimeField(
        read_only=True, help_text="Timestamp when review was completed"
    )


class ArticleApproveResponseSerializer(serializers.Serializer):
    """Response for article approval"""

    article_status = serializers.CharField(
        read_only=True, help_text="Article status (should be 'ready_for_publishing')"
    )
    assigned_editor = WorkflowUserSerializer(
        read_only=True, help_text="Editor assigned to publish the article"
    )
    completed_at = serializers.DateTimeField(
        read_only=True, help_text="Timestamp when review was completed"
    )


class LiveblocksAuthRequestSerializer(serializers.Serializer):
    """Validate Liveblocks authentication request"""

    room_id = serializers.CharField(
        required=True, help_text="Liveblocks room ID (e.g., 'article-123')"
    )

    def validate_room_id(self, value):
        """Validate room format"""
        if not value.startswith("article-"):
            raise serializers.ValidationError(
                "Invalid room format. Expected format: 'article-{id}'"
            )
        return value


class LiveblocksAuthResponseSerializer(serializers.Serializer):
    """Liveblocks authentication response"""

    token = serializers.CharField(
        read_only=True, help_text="JWT token for Liveblocks authentication"
    )
    user_id = serializers.CharField(read_only=True, help_text="User ID for Liveblocks")


class ArticleForReviewSerializer(serializers.ModelSerializer):
    """Nested article data for review listings"""

    author = UserSerializer(read_only=True)
    liveblocks_room_id = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "status",
            "author",
            "created_at",
            "updated_at",
            "liveblocks_room_id",
        ]

    @extend_schema_field(serializers.CharField)
    def get_liveblocks_room_id(self, obj):
        return f"article-{obj.id}"


class ReviewListSerializer(serializers.ModelSerializer):
    """Serializer for listing reviews (compact view)"""

    article = ArticleForReviewSerializer(read_only=True)
    reviewed_by = UserSerializer(read_only=True)

    class Meta:
        model = ArticleReview
        fields = [
            "id",
            "article",
            "reviewed_by",
            "status",
            "started_at",
            "completed_at",
        ]
        read_only_fields = ["id"]


class ArticleDetailForReviewSerializer(serializers.ModelSerializer):
    """Full article data for review detail view"""

    author = UserSerializer(read_only=True)
    assigned_reviewer = UserSerializer(read_only=True)
    assigned_editor = UserSerializer(read_only=True)
    liveblocks_room_id = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "cover_image_url",
            "status",
            "author",
            "assigned_reviewer",
            "assigned_editor",
            "created_at",
            "updated_at",
            "liveblocks_room_id",
            "content_last_synced_at",
        ]

    @extend_schema_field(serializers.CharField)
    def get_liveblocks_room_id(self, obj):
        return f"article-{obj.id}"

    @extend_schema_field(serializers.URLField)
    def get_cover_image_url(self, obj):
        """Get article cover image URL"""
        return obj.cover_image_url


class WorkflowHistorySerializer(serializers.ModelSerializer):
    """Serializer for workflow history entries"""

    changed_by = UserSerializer(read_only=True)

    class Meta:
        model = ArticleWorkflowHistory
        fields = [
            "id",
            "from_status",
            "to_status",
            "changed_by",
            "changed_at",
            "notes",
        ]


class ReviewDetailSerializer(serializers.ModelSerializer):
    """Detailed view of a review with full article data and history"""

    article = ArticleDetailForReviewSerializer(read_only=True)
    reviewed_by = UserSerializer(read_only=True)
    workflow_history = serializers.SerializerMethodField()
    reviewer_notes = serializers.SerializerMethodField()

    class Meta:
        model = ArticleReview
        fields = [
            "id",
            "article",
            "reviewed_by",
            "status",
            "started_at",
            "completed_at",
            "reviewer_notes",
            "workflow_history",
        ]
        read_only_fields = ["id"]

    @extend_schema_field(WorkflowHistorySerializer(many=True))
    def get_workflow_history(self, obj):
        """Get recent workflow history for the article"""
        history = obj.article.workflow_history.select_related(
            "changed_by", "article"
        ).all()[:10]
        return WorkflowHistorySerializer(history, many=True).data

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_reviewer_notes(self, obj):
        """Only show reviewer_notes to the reviewer themselves"""
        request = self.context.get("request")
        if request and request.user == obj.reviewed_by:
            return obj.reviewer_notes
        return None  # Hide from article author and others


# NOTE: MIGHT REMOVE READ-ONLY IN SOME IF IT IS JUST GET AND NO PUT/PATCH
