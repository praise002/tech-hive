from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from . import models


class NotificationSerializer(serializers.ModelSerializer):
    actor_name = serializers.SerializerMethodField()
    recipient_name = serializers.SerializerMethodField()

    class Meta:
        model = models.Notification
        fields = ["id", "actor_name", "recipient_name", "verb", "is_read", "created_at"]

    @extend_schema_field(serializers.CharField)
    def get_actor_name(self, obj):
        return obj.actor.full_name if obj.actor else None

    @extend_schema_field(serializers.CharField)
    def get_recipient_name(self, obj):
        return obj.recipient.full_name if obj.recipient else None
