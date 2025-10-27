from apps.accounts.models import ContributorOnboarding
from apps.content import models
from apps.content.CustomRelations import CustomHyperlinkedIdentityField
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


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
    is_reply = serializers.SerializerMethodField()

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


# TODO: Still try to understand it
# class CommentCreateSerializer(serializers.ModelSerializer):
#     replying_to = serializers.UUIDField(required=False, write_only=True)

#     class Meta:
#         model = models.Comment
#         fields = ["article", "body", "parent", "replying_to"]

#     def create(self, validated_data):
#         user = self.context["request"].user
#         replying_to_id = validated_data.pop("replying_to", None)
#         # Get the parent comment to determine who we're replying to
#         parent_comment = validated_data.get("parent")

#         # AUTO-MENTION LOGIC: If replying_to not provided but we have a parent, use parent's author
#         if not replying_to_id and parent_comment:
#             replying_to_id = parent_comment.user_id

#         comment = models.Comment.objects.create(user=user, **validated_data)

#         # Set who we're replying to (either explicitly provided or auto-detected from parent)

#         if replying_to_id:
#             try:
#                 from apps.accounts.models import User

#                 replying_to_user = User.objects.get(id=replying_to_id)
#                 comment.replying_to = replying_to_user
#                 comment.save()
#             except User.DoesNotExist:
#                 pass  # Silently fail if user doesn't exist

#         return comment


class ArticleCommentSerializer(serializers.ModelSerializer):
    """Serializer for displaying comments on articles with lazy-loading support"""

    user_name = serializers.CharField(source="user.full_name", read_only=True)
    user_avatar = serializers.URLField(source="user.avatar_url", read_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)
    reply_count = serializers.SerializerMethodField(read_only=True)
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
            "reply_count",
        ]

    @extend_schema_field(serializers.IntegerField)
    def get_reply_count(self, obj):
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
            if comment.thread is not None and comment.thread.root_comment_id == comment.id
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


class CommentWithRepliesSerializer(serializers.ModelSerializer):
    """Serializer for fetching replies of a specific comment"""

    user_name = serializers.CharField(source="user.full_name", read_only=True)
    user_avatar = serializers.URLField(source="user.avatar_url", read_only=True)
    user_username = serializers.CharField(source="user.username", read_only=True)
    reply_count = serializers.SerializerMethodField(read_only=True)

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
            "reply_count",
            "replying_to_name",
            "replying_to_username",
        ]

    @extend_schema_field(serializers.IntegerField)
    def get_reply_count(self, obj):
        """Count active replies for this comment"""
        return obj.get_all_replies_count()


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
