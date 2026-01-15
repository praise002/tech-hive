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
    role = serializers.SerializerMethodField()

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
            "role",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "email": {"read_only": True},
        }

    @extend_schema_field(serializers.URLField)
    def get_avatar_url(self, obj):
        return obj.avatar_url
    
    @extend_schema_field(serializers.CharField)
    def get_role(self, obj):
        group = obj.groups.first()
        return group.name if group else None


class AvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "avatar",
        ]
