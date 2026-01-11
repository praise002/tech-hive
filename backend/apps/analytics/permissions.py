from apps.accounts.utils import UserRoles
from rest_framework.permissions import BasePermission


class IsAuthorOrAdmin(BasePermission):
    """
    User must be either:
    - Author (in CONTRIBUTOR group and owns the object)
    - OR Admin (is_staff=True)
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return (
            request.user.is_staff
            or request.user.groups.filter(name=UserRoles.CONTRIBUTOR).exists()
        )

    def has_object_permission(self, request, view, obj):

        if request.user.is_staff:
            return True

        return obj.author == request.user
