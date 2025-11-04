from apps.accounts.models import User
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
        ]


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "created_at",
            "avatar_url",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "email": {"read_only": True},
        }

    @extend_schema_field(serializers.URLField)
    def get_avatar_url(self, obj):
        return obj.avatar_url


class AvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "avatar",
        ]
