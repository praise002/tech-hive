from apps.accounts.utils import UserRoles
from rest_framework import permissions
from rest_framework.permissions import BasePermission

from .models import Article, ArticleReview


class IsContributor(BasePermission):
    """
    Permission for Contributors:
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.groups.filter(name=UserRoles.CONTRIBUTOR).exists()


class IsAuthorOrReadOnly(BasePermission):
    """
    Permission that allows authors to edit their own articles and others to read only.
    """

    def has_permission(self, request, view):
        # Read permissions for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for authenticated users
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for article author
        if isinstance(obj, Article):
            return obj.author == request.user

        return False


class CanSubmitForReview(BasePermission):
    """
    Permission to submit articles for review.
    Only article authors can submit their own articles.
    """

    # def has_permission(self, request, view):
    #     return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Article):
            return obj.author == request.user
        return False


class CanManageReview(BasePermission):
    """
    Permission to manage article reviews (change status, add feedback).
    Only assigned reviewers can manage reviews for specific articles.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Must have reviewer role
        return request.user.groups.filter(name=UserRoles.REVIEWER).exists()

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Article):
            # Must be assigned as reviewer for this article
            return obj.reviews.filter(reviewed_by=request.user, is_active=True).exists()

        if isinstance(obj, ArticleReview):
            # Must be the assigned reviewer
            return obj.reviewed_by == request.user

        return False


class CanPublishArticle(BasePermission):
    """
    Permission to publish articles.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Must have editor role
        return request.user.groups.filter(name=UserRoles.EDITOR).exists()

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Article):
            return obj.assigned_editor == request.user

        return False


class IsCommentAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
