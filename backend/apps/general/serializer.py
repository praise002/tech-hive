from apps.general.models import Contact, Newsletter, SiteDetail
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class NewsletterSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        model = Newsletter
        fields = ["email"]

    def validate_email(self, value):
        """Check if email is already subscribed"""
        email = value.lower().strip()

        if Newsletter.objects.filter(email=email, is_subscribed=True).exists():
            raise serializers.ValidationError(
                "This email is already subscribed to the newsletter."
            )

        return email

    def create(self, validated_data):
        email = validated_data.get("email")
        instance, created = Newsletter.objects.get_or_create(
            email=email, defaults=validated_data
        )

        if not created:
            # If it already exists, it must be unsubscribed (due to validate_email check)
            # So we re-subscribe them
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.is_subscribed = True
            instance.unsubscribed_at = None
            instance.save()

        return instance


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
