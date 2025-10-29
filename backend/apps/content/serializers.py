from apps.accounts.models import ContributorOnboarding
from apps.content import models
from apps.content.CustomRelations import CustomHyperlinkedIdentityField
from apps.content.models import Article, Comment, CommentThread
from apps.content.utils import ArticleStatusChoices
from django.db.models import F
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied


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
    cover_image_url = serializers.SerializerMethodField(read_only=True)
    read_time = serializers.SerializerMethodField(read_only=True)
    author = serializers.SerializerMethodField(read_only=True)
    total_reaction_counts = serializers.SerializerMethodField(read_only=True)
    reaction_counts = serializers.SerializerMethodField(read_only=True)

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
    url = CustomHyperlinkedIdentityField(
        view_name="article_detail",
        lookup_fields=[
            (
                "author.username",
                "username",
            ),  # Get username from article.author.username
            ("slug", "slug"),  # Get slug from article.slug
        ],
    )

    class Meta:
        model = models.Article
        fields = [
            "title",
            "content",
            "url",
        ]
        # TODO: Editor will add it to the right category

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
            "content",
        ]


class ArticleAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = [
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
    article_created_at = serializers.DateTimeField(
        source="article.created_at", read_only=True
    )
    user_id = serializers.SerializerMethodField()

    replying_to_username = serializers.CharField(
        source="replying_to.username", read_only=True
    )

    class Meta:
        model = models.Comment
        fields = [
            "id",
            "user_id",
            "article_id",
            "article_title",
            "article_created_at",
            "body",
            "replying_to_username",
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
            article = Article.objects.get(id=data["article_id"])
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

    # TODO: replying_to logic later
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
                self.thread.reply_count += 1
                CommentThread.objects.filter(id=self.thread.id).update(
                    reply_count=F("reply_count") + 1
                )

                self.thread.refresh_from_db()

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

        return comment


class CommentResponseSerializer(serializers.ModelSerializer):
    """Serializer for returning comment data after creation"""

    user_name = serializers.CharField(source="user.full_name", read_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)
    user_avatar = serializers.URLField(source="user.avatar_url", read_only=True)
    thread_id = serializers.UUIDField(source="thread.id", read_only=True)
    is_root = serializers.SerializerMethodField(read_only=True)

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
    total_replies = serializers.SerializerMethodField(read_only=True)
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
    comments = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)

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

    replying_to_name = serializers.CharField(
        source="replying_to.full_name", read_only=True
    )
    replying_to_username = serializers.CharField(
        source="replying_to.username", read_only=True
    )

    class Meta:
        model = models.Comment
        fields = [
            "id",
            "body",
            "created_at",
            "user_name",
            "user_username",
            "user_avatar",
            "replying_to_name",
            "replying_to_username",
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
    image_url = serializers.SerializerMethodField(read_only=True)

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


# TODO: MIGHT REMOVE READ-ONLY IN SOME IF IT IS JUST GET AND NO PUT/PATCH
# TODO: MIGHT REMOVE READ-ONLY IN SOME IF IT IS JUST GET AND NO PUT/PATCH
# TODO: MIGHT REMOVE READ-ONLY IN SOME IF IT IS JUST GET AND NO PUT/PATCH
