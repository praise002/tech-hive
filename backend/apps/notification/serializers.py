from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from . import models


class NotificationSerializer(serializers.ModelSerializer):
    actor_name = serializers.SerializerMethodField()
    recipient_name = serializers.SerializerMethodField()
    actor_avatar = serializers.SerializerMethodField()
    target_content_type = serializers.SerializerMethodField()
    target_object_id = serializers.CharField(source="target_id", read_only=True)
    target_slug = serializers.SerializerMethodField()
    target_username = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = models.Notification
        fields = [
            "id",
            "actor_name",
            "actor_avatar",
            "recipient_name",
            "verb",
            "description",
            "target_content_type",
            "target_object_id",
            "target_slug",
            "target_username",
            "is_read",
            "is_deleted",
            "created_at",
        ]

    @extend_schema_field(serializers.CharField)
    def get_description(self, obj):
        actor = obj.actor.full_name if obj.actor else "Someone"
        return f"{actor} {obj.verb}"

    @extend_schema_field(serializers.CharField)
    def get_actor_name(self, obj):
        return obj.actor.full_name if obj.actor else None

    @extend_schema_field(serializers.URLField)
    def get_actor_avatar(self, obj):
        if obj.actor and hasattr(obj.actor, "avatar_url"):
            return obj.actor.avatar_url
        return None

    @extend_schema_field(serializers.CharField)
    def get_recipient_name(self, obj):
        return obj.recipient.full_name if obj.recipient else None

    @extend_schema_field(serializers.CharField)
    def get_target_content_type(self, obj):
        return obj.target_ct.model if obj.target_ct else None

    @extend_schema_field(serializers.CharField)
    def get_target_slug(self, obj):
        if obj.target and hasattr(obj.target, "slug"):
            return obj.target.slug
        return None

    @extend_schema_field(serializers.CharField)
    def get_target_username(self, obj):
        # Specific logic for objects that link to a user profile via 'author'
        if obj.target and hasattr(obj.target, "author"):
            return obj.target.author.username
        return None
