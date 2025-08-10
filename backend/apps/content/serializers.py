from apps.content import models
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ["id", "name"]


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

    def get_author(self, obj):
        return obj.author.full_name

    def get_total_reaction_counts(self, obj):
        return obj.total_reaction_counts

    def get_reaction_counts(self, obj):
        return obj.reaction_counts


class ArticleCreateDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = [
            "title",
            "content",
        ]
        # TODO: Editor will add it to the right category

    def create(self, validated_data):
        # Get the authenticated user's profile
        user = self.context["request"].user

        # Create the author and associate it with the user
        article = models.Article.objects.create(author=user, **validated_data)
        return article


class ArticleAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = [
            "cover_image",
        ]


class ArticleReaction(serializers.ModelSerializer):
    # For POST/PUT/PATCH
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all())

    class Meta:
        model = models.ArticleReaction
        fields = ["id", "user", "article", "reaction_type"]


class SavedArticle(serializers.ModelSerializer):
    class Meta:
        model = models.SavedArticle
        fields = ["id", "user", "article"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ["id", "user", "article", "text"]


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
