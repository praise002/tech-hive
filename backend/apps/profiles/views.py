import logging

from apps.accounts.models import User
from apps.common.errors import ErrorCode
from apps.common.exceptions import NotFoundError
from apps.common.pagination import DefaultPagination
from apps.common.responses import CustomResponse
from apps.content.filters import UserArticleFilter
from apps.content.mixins import HeaderMixin
from apps.content.models import Article, ArticleStatusChoices, Comment, SavedArticle
from apps.content.permissions import IsContributor
from apps.content.serializers import (
    ArticleCreateSerializer,
    ArticleSerializer,
    ArticleUpdateSerializer,
    CommentSerializer,
    SaveArticleCreateSerializer,
    SavedArticleSerializer,
)
from apps.profiles.schema_examples import (
    ACCOUNT_DEACTIVATE_RESPONSE_EXAMPLE,
    ACCOUNT_REACTIVATE_RESPONSE_EXAMPLE,
    ARTICLE_CREATE_RESPONSE_EXAMPLE,
    ARTICLE_DETAIL_RESPONSE_EXAMPLE,
    ARTICLE_LIST_EXAMPLE,
    ARTICLE_UPDATE_RESPONSE_EXAMPLE,
    AVATAR_UPDATE_RESPONSE_EXAMPLE,
    COMMENTS_ARTICLES_RESPONSE_EXAMPLE,
    PROFILE_DETAIL_RESPONSE_EXAMPLE,
    PROFILE_RETRIEVE_RESPONSE_EXAMPLE,
    PROFILE_UPDATE_RESPONSE_EXAMPLE,
    SAVED_ARTICLES_CREATE_RESPONSE_EXAMPLE,
    SAVED_ARTICLES_RESPONSE_EXAMPLE,
    USERNAMES_RESPONSE_EXAMPLE,
)
from apps.profiles.serializers import (
    AvatarSerializer,
    UsernameSerializer,
    UserSerializer,
)
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
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


class UsernameListView(ListAPIView):
    serializer_class = UsernameSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        return Comment.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data)
            return CustomResponse.success(
                message="Usernames retrieved successfully.",
                data=paginated_data.data,
                status_code=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message="Usernames retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Retrieve user's usernames",
        description="This endpoint retrieves a list of usernames. It's primarily used to populate the user mention feature in the comment section.",
        tags=tags,
        responses=USERNAMES_RESPONSE_EXAMPLE,
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProfileView(APIView):
    """
    View to retrieve the authenticated user's profile.
    """

    serializer_class = UserSerializer
    permission_classes = (
        IsAuthenticated,
    )  # Only the user should be able to view their own profile

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
        # request=build_avatar_request_schema(),
        request={
            "multipart/form-data": AvatarSerializer,
        },
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


class UserArticleListCreateView(ListCreateAPIView):
    queryset = Article.objects.select_related("author").prefetch_related("tags")

    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserArticleFilter

    search_fields = ["title", "content"]
    pagination_class = DefaultPagination
    permission_classes = (IsContributor,)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ArticleCreateSerializer
        return ArticleSerializer

    def get_queryset(self):
        """
        Filter articles to only return those belonging to the authenticated user.
        """
        return self.queryset.filter(author=self.request.user)

    @extend_schema(
        summary="Retrieve a list of user articles",
        description="This endpoint allows authenticated users to retrieve a paginated list of their own articles. It allows filtering articles",
        parameters=[
            OpenApiParameter(
                name="status",
                description="Filter articles by status.",
                enum=[  # it has to be specified for it to wrok
                    "draft",
                    "submitted",
                    "submitted_for_review",
                    "under_review",
                    "changes_requested",
                    "review_completed",
                    "ready_for_publishing",
                    "published",
                    "rejected",
                ],
            ),
            OpenApiParameter(
                name="search",
                description="Search across title, and content.",
            ),
        ],
        tags=tags,
        responses=ARTICLE_LIST_EXAMPLE,
    )
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve articles with pagination, and search.
        """
        return super().get(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data)
            return CustomResponse.success(
                message="Articles retrieved successfully.",
                data=paginated_data.data,
                status_code=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message="Articles retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Create a new article",
        description="This endpoint allows authenticated contributors to create a new article draft. ",
        tags=tags,
        responses=ARTICLE_CREATE_RESPONSE_EXAMPLE,
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)

        return CustomResponse.success(
            message="Article created successfully.",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED,
            headers=headers,
        )


class ArticleRetrieveUpdateView(HeaderMixin, APIView):
    permission_classes = (IsContributor,)

    def get_object_for_read(self, slug):
        """Get object for GET requests - filtering logic"""
        try:
            # permission takes care of getting the specific user
            obj = Article.objects.select_related("author").get(
                slug=slug,
                status__in=[
                    ArticleStatusChoices.DRAFT,
                    ArticleStatusChoices.CHANGES_REQUESTED,
                    ArticleStatusChoices.SUBMITTED_FOR_REVIEW,
                    ArticleStatusChoices.UNDER_REVIEW,
                    ArticleStatusChoices.READY,
                    ArticleStatusChoices.REJECTED,
                ],
            )

            self.check_object_permissions(self.request, obj)
            return obj
        except Article.DoesNotExist:
            raise NotFoundError(err_msg="Article not found.")

    def get_object_for_write(self, slug):
        """Get object for PATCH requests - permissions will handle edit restrictions"""
        try:
            obj = Article.objects.select_related("author").get(
                slug=slug,
            )
            self.check_object_permissions(self.request, obj)

            return obj
        except Article.DoesNotExist:
            raise NotFoundError(err_msg="Article not found.")

    def get_serializer_class(self, request=None):
        """
        Helper method to select serializer class based on request method.
        """
        if request and request.method != "GET":
            return ArticleUpdateSerializer
        return ArticleSerializer

    def get_serializer(self, *args, **kwargs):
        """
        Helper to get an instance of the correct serializer.
        """
        serializer_class = self.get_serializer_class(
            kwargs.get("request") or self.request
        )
        return serializer_class(*args, **kwargs)

    @extend_schema(
        summary="Retrieve article details",
        description="Retrieve detailed information about a specific article using the author's username and article slug.",
        tags=tags,
        responses=ARTICLE_DETAIL_RESPONSE_EXAMPLE,
    )
    def get(self, *args, **kwargs):
        try:
            article = self.get_object_for_read(slug=kwargs["slug"])

            serializer = self.get_serializer(article)
            return CustomResponse.success(
                message="Article detail retrieved successfully.",
                data=serializer.data,
                status_code=status.HTTP_200_OK,
            )

        except Article.DoesNotExist:
            raise NotFoundError(err_msg="Article not found.")

    @extend_schema(
        summary="Update article",
        description="Update an existing article using partial data. Only the article author can modify articles.",
        tags=tags,
        responses=ARTICLE_UPDATE_RESPONSE_EXAMPLE,
    )
    def patch(self, request, *args, **kwargs):
        article = self.get_object_for_write(slug=kwargs["slug"])
        serializer = self.get_serializer(article, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        headers = self.get_success_headers(serializer.data)

        return CustomResponse.success(
            message="Article updated successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
            headers=headers,
        )


class SavedArticlesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return SaveArticleCreateSerializer
        return SavedArticleSerializer

    def get_serializer(self, *args, **kwargs):
        """
        Helper to get an instance of the correct serializer.
        """
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_queryset(self):
        """Filter saved articles to only return those belonging to the authenticated user."""
        return SavedArticle.published.filter(user=self.request.user).select_related(
            "article", "user"
        )

    @extend_schema(
        summary="Retrieve user's saved articles",
        description="This endpoint allows authenticated users to retrieve a list of articles they have saved. Only the user's own saved articles are returned.",
        tags=tags,
        responses=SAVED_ARTICLES_RESPONSE_EXAMPLE,
    )
    def get(self, *args, **kwargs):
        saved_articles = self.get_queryset()
        serializer = self.get_serializer(saved_articles, many=True)

        return CustomResponse.success(
            message="Saved Articles retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Save or unsave an article",
        description="Toggle save status for an article. If article is not saved, it will be saved. If already saved, it will be unsaved.",
        tags=tags,
        responses=SAVED_ARTICLES_CREATE_RESPONSE_EXAMPLE,
    )
    def post(self, request):
        """Save or unsave an article for the authenticated user."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        article = serializer.article
        if article.status != ArticleStatusChoices.PUBLISHED:
            return CustomResponse.error(
                message="You can only save or unsave an article that is published.",
                err_code=ErrorCode.UNPROCESSABLE_ENTITY,
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        # Toggle save status
        saved_article, created = SavedArticle.objects.get_or_create(
            user=request.user, article=article
        )

        if created:
            return CustomResponse.success(
                message="Article saved successfully",
                status_code=status.HTTP_201_CREATED,
            )
        else:
            saved_article.delete()
            return CustomResponse.success(
                message="Article unsaved successfully", status_code=status.HTTP_200_OK
            )


class UserCommentsView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Filter saved articles to only return those belonging to the authenticated user."""
        return Comment.objects.filter(
            user=self.request.user, active=True
        ).select_related("article", "user", "replying_to")

    @extend_schema(
        summary="Retrieve user's comments",
        description="This endpoint allows authenticated users to retrieve a list of all comments they have made across different articles.",
        tags=tags,
        responses=COMMENTS_ARTICLES_RESPONSE_EXAMPLE,
    )
    def get(self, *args, **kwargs):
        comments = self.get_queryset()
        serializer = self.serializer_class(comments, many=True)

        return CustomResponse.success(
            message="Comments retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class UserCommentsGenericView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        """Filter saved articles to only return those belonging to the authenticated user."""
        return Comment.objects.filter(
            user=self.request.user, is_active=True
        ).select_related("article", "user")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.get_paginated_response(serializer.data)
            return CustomResponse.success(
                message="Comments retrieved successfully.",
                data=paginated_data.data,
                status_code=status.HTTP_200_OK,
            )

        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(
            message="Comments retrieved successfully.",
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Retrieve user's comments",
        description="This endpoint allows authenticated users to retrieve a list of all comments they have made across different articles.",
        tags=tags,
        responses=COMMENTS_ARTICLES_RESPONSE_EXAMPLE,
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
