from apps.accounts.utils import UserRoles
from apps.content.choices import ArticleStatusChoices
from rest_framework import permissions
from rest_framework.permissions import BasePermission

from .models import Article, ArticleReview, Category


class CustomBasePermission(BasePermission):
    """
    Base permission class for Tech Hive role-based access control.

    - Allows read access to everyone
    - Restricts write operations to authenticated users with platform roles
    - Should be inherited by specific role permission classes

    Returns:
        bool: Permission granted/denied
    """

    def has_permission(self, request, view):
        # Allow read access to everyone for published articles
        if request.method in permissions.SAFE_METHODS:
            return True

        # For write operations, user must be authenticated and have these roles
        if not request.user.is_authenticated:
            return False

        return request.user.groups.filter(
            name__in=[
                UserRoles.CONTRIBUTOR,
                UserRoles.REVIEWER,
                UserRoles.EDITOR,
                UserRoles.MANAGER,
            ]
        ).exists()


class IsPublished(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Article):
            return obj.status in [
                ArticleStatusChoices.PUBLISHED,
            ]

        return False


class IsContributor(BasePermission):
    """
    Permission for Contributors:
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.groups.filter(name=UserRoles.CONTRIBUTOR).exists()

    # def has_object_permission(self, request, view, obj):
    #     if isinstance(obj, Article):
    #         # Read permissions - contributors can view their own articles
    #         if request.method in permissions.SAFE_METHODS:
    #             return obj.author == request.user

    #         # Contributors can only edit their own drafts
    #         return obj.author == request.user and obj.status in [
    #             ArticleStatusChoices.DRAFT,
    #             ArticleStatusChoices.CHANGES_REQUESTED,
    #             ArticleStatusChoices.REJECTED,
    #         ]

        # return False

# TODO: CONFUSING
# class IsReviewerOrReadOnly(CustomBasePermission):
#     """
#     Permission for Reviewers:
#     - Can view articles assigned for review
#     - Can change article status during review process
#     - Can create and manage article reviews
#     """

#     def has_object_permission(self, request, view, obj):
#         # Read permissions
#         if request.method in permissions.SAFE_METHODS:
#             if isinstance(obj, Article):
#                 # Can read published articles
#                 if obj.status == ArticleStatusChoices.PUBLISHED:
#                     return True
#                 # Can read articles assigned for review
#                 if obj.reviews.filter(
#                     reviewed_by=request.user
#                 ).exists():
#                     return True

#             if isinstance(obj, ArticleReview):
#                 # Can read own reviews or if they're the article author
#                 return (
#                     obj.reviewed_by == request.user
#                     or obj.article.author == request.user
#                 )

#             return True

#         # Write permissions
#         if isinstance(obj, Article):

#             # Articles assigned for review
#             if obj.reviews.filter(reviewed_by=request.user, is_active=True).exists():
#                 return obj.status in [
#                     ArticleStatusChoices.SUBMITTED_FOR_REVIEW,
#                     ArticleStatusChoices.UNDER_REVIEW,
#                     ArticleStatusChoices.CHANGES_REQUESTED,
#                 ]

#         if isinstance(obj, ArticleReview):
#             # Can modify own reviews
#             return obj.reviewed_by == request.user

#         return False


class IsEditorOrReadOnly(CustomBasePermission):  # Access to admin interface
    """
    Permission for Editors:
    - Can publish articles
    - Can add tags to articles
    - Can assign reviewers to articles
    - Can view articles ready for publishing
    - Can add published articles to categories
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions
        if request.method in permissions.SAFE_METHODS:
            if isinstance(obj, Article):
                # Can read all articles for editorial purposes
                return True

            if isinstance(obj, ArticleReview):
                return True

            return True

        # Write permissions
        if isinstance(obj, Article):

            # Can publish articles that are ready
            # Can add tags to articles ready for publishing or published
            if obj.status in [
                ArticleStatusChoices.READY,
                ArticleStatusChoices.PUBLISHED,
            ]:
                return True

            # Can assign reviewers and manage editorial workflow
            # Can add articles to categories (modify category field)
            return True

        if isinstance(obj, ArticleReview):
            # Can create and manage all reviews
            return True

        if isinstance(obj, Category):
            # Editors can manage categories for all articles
            return True

        return False


class IsManagerOrReadOnly(CustomBasePermission):
    """
    Permission for Managers:
    - Full access to user management through views (handled in views)
    - Access to platform statistics
    """

    def has_object_permission(self, request, view, obj):
        # Managers have full access to content management
        return True


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
    Only editors and above can publish articles that are ready for publishing.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Must have editor role or higher
        return request.user.groups.filter(name=UserRoles.EDITOR).exists()

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Article):
            # Can only publish articles that are ready
            return obj.status == ArticleStatusChoices.READY

        return False


class IsCommentAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
