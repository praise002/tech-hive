from apps.general.models import Contact, Newsletter, SiteDetail
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = ["email"]


class SiteDetailSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SiteDetail
        fields = ["image_url", "body", "fb", "ln", "x", "ig"]

    @extend_schema_field(serializers.URLField)
    def get_image_url(self, obj):
        return obj.image_url


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["name", "email", "content"]
