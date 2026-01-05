from apps.analytics.choices import DeviceTypeChoices, EventTypeChoices
from apps.common.serializers import SuccessResponseSerializer
from rest_framework import serializers


class TrackActivityRequestSerializer(serializers.Serializer):
    event_type = serializers.ChoiceField(choices=EventTypeChoices.choices)
    session_id = serializers.CharField(max_length=255)
    page_url = serializers.URLField()
    referrer = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    device_type = serializers.ChoiceField(
        choices=DeviceTypeChoices.choices, required=False
    )
    browser = serializers.CharField(max_length=100, required=False)
    browser_version = serializers.CharField(max_length=50, required=False)
    os = serializers.CharField(max_length=100, required=False)
    os_version = serializers.CharField(max_length=50, required=False)
    screen_resolution = serializers.CharField(max_length=50, required=False)
    duration_seconds = serializers.IntegerField(min_value=0, default=0)
    load_time_ms = serializers.IntegerField(
        min_value=0, required=False, allow_null=True
    )
    metadata = serializers.JSONField(required=False, default=dict)

    def validate_metadata(self, value):
        """
        Ensure metadata contains required fields for certain event types
        """
        event_type = self.initial_data.get("event_type")

        # For page_view, share, reaction events on content
        if event_type in ["page_view", "share", "page_load"]:
            if "content_type" not in value or "content_id" not in value:
                raise serializers.ValidationError(
                    "metadata must contain 'content_type' and 'content_id' for this event type"
                )

        return value


class DeviceDistributionSerializer(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.IntegerField(min_value=0)
    percentage = serializers.FloatField()


class ActiveUserTimelineSerializer(serializers.Serializer):
    date = serializers.DateField()
    day = serializers.CharField()
    registered_users = serializers.IntegerField(min_value=0)
    visitors = serializers.IntegerField(min_value=0)
    total_active_users = serializers.IntegerField(min_value=0)


class DashboardMetricsSerializer(serializers.Serializer):
    period = serializers.CharField()
    date_range = serializers.DictField()
    metrics = serializers.DictField()
    device_types = DeviceDistributionSerializer(many=True)
    active_users = ActiveUserTimelineSerializer(many=True)
    top_performing_posts = serializers.DictField()
    cached = serializers.BooleanField()


class SuccessResponseDataSerializer(SuccessResponseSerializer):
    data = serializers.DictField()
