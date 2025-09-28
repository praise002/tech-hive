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
    article_id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = models.SavedArticle
        fields = ["id", "user_id", "article_id"]

    def get_article_id(self, obj):
        return str(obj.article.id)

    def get_user_id(self, obj):
        return str(obj.user.id)


class SaveArticleCreateSerializer(serializers.Serializer):
    """Serializer for saving/unsaving articles"""

    article_id = serializers.UUIDField()

    def validate_article_id(self, article_id):
        """Validate that the article exists and is published"""
        try:
            article = models.Article.objects.get(
                id=article_id
            )
        except models.Article.DoesNotExist:
            raise serializers.ValidationError("Article not found")

        self.article = article 
        
        return article_id


class CommentSerializer(serializers.ModelSerializer):
    article_id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    class Meta:
        model = models.Comment
        fields = ["id", "user_id", "article_id", "body"]
        
    def get_article_id(self, obj):
        return str(obj.article.id)

    def get_user_id(self, obj):
        return str(obj.user.id)


class JobSerializer(serializers.ModelSerializer):
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
        ]


class EventSerializer(serializers.ModelSerializer):
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
        ]


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Resource
        fields = ["id", "name", "image_url", "body", "url"]


class ToolTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ToolTag
        fields = ["id", "name"]


class ToolSerializer(serializers.ModelSerializer):
    tags = ToolTagSerializer(many=True, read_only=True)

    class Meta:
        model = models.Tool
        fields = ["id", "name", "desc", "url", "image_url", "call_to_action", "tags"]


# TODO: MIGHT REMOVE READ-ONLY IN SOME IF IT IS JUST GET AND NO PUT/PATCH
