import logging

from apps.accounts.models import User
from apps.common.exceptions import NotFoundError
from apps.common.responses import CustomResponse
from apps.profiles.schema_examples import (
    AVATAR_UPDATE_RESPONSE_EXAMPLE,
    PROFILE_DETAIL_RESPONSE_EXAMPLE,
    PROFILE_RETRIEVE_RESPONSE_EXAMPLE,
    PROFILE_UPDATE_RESPONSE_EXAMPLE,
    build_avatar_request_schema,
)
from apps.profiles.serializers import AvatarSerializer, UserSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

tags = ["Profiles"]

logger = logging.getLogger(__name__)
security_logger = logging.getLogger("security")


class ProfileView(APIView):
    """
    View to retrieve the authenticated user's profile.
    """

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)  #Only the user should be able to view their own profile

    @extend_schema(
        summary="View a user profile",
        description="This endpoint allows authenticated users to view their profile details. Users can retrieve their account information. Only the account owner can access their profile.",
        tags=tags,
        responses=PROFILE_RETRIEVE_RESPONSE_EXAMPLE,
    )
    def get(self, request):
        profile = request.user
        serializer = self.serializer_class(profile)
        return CustomResponse.success(
            message="Profile retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Update user profile",
        description="This endpoint allows authenticated users to edit their profile details. Users can update their personal information. Only the account owner can modify their profile.",
        tags=tags,
        responses=PROFILE_UPDATE_RESPONSE_EXAMPLE,
    )
    def patch(self, request):
        profile = request.user
        serializer = self.serializer_class(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()

        return CustomResponse.success(
            message="Profile updated successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class ProfileViewGeneric(RetrieveUpdateAPIView):
    """
    View to retrieve and update the authenticated user's profile.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = [
        "get",
        "patch",
        "head",
        "options",
    ]  # to remove the put method inherited from RetrieveUpdate

    def get_object(self):
        """
        Return the profile of the authenticated user.
        """
        return self.request.user

    @extend_schema(
        summary="View a user profile",
        description="This endpoint allows authenticated users to view their profile details. Users can retrieve their account information. Only the account owner can access their profile.",
        tags=tags,
        responses=PROFILE_RETRIEVE_RESPONSE_EXAMPLE,
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve the authenticated user's profile.
        """
        return self.retrieve(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.success(
            message="Profile retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Update user profile",
        description="This endpoint allows authenticated users to edit their profile details. Users can update their personal information. Only the account owner can modify their profile.",
        tags=tags,
        responses=PROFILE_UPDATE_RESPONSE_EXAMPLE,
    )
    def patch(self, request, *args, **kwargs):
        """
        Partially update the authenticated user's profile.
        """
        return self.partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Override the update method to customize the response format.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return CustomResponse.success(
            message="Profile updated successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


# My reason for ProfileView and PublicProfileView is because the frontend will need to get
# current logged in user with /user so putting .username in the url will be a problem


class PublicProfileView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_object(self):
        username = self.kwargs.get("username")
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFoundError("User profile not found.")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.success(
            message="Profile retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Retrieve a user's public profile",
        description="This endpoint allows anyone to view a user's public profile details.  It retrieves account information based on the user's ID.",
        tags=tags,
        responses=PROFILE_DETAIL_RESPONSE_EXAMPLE,
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class AvatarUpdateView(APIView):
    serializer_class = AvatarSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Update user avatar",
        description="This endpoint allows authenticated users to upload or update their profile avatar.",
        tags=tags,
        request=build_avatar_request_schema(),
        responses=AVATAR_UPDATE_RESPONSE_EXAMPLE,
    )
    def patch(self, request):
        profile = request.user
        serializer = self.serializer_class(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()

        return CustomResponse.success(
            message="Profile avatar updated successfully.",
            data={
                "avatar_url": profile.avatar_url,
            },
            status_code=status.HTTP_200_OK,
        )


class UserArticleListCreateView(APIView):
    # user published article + draft creation
    pass


class SavedArticlesView(APIView):
    # user saved articles
    pass


class UserCommentsView(APIView):
    # user comments
    pass
