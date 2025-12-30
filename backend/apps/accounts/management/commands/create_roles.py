from apps.accounts.models import User
from apps.accounts.utils import UserRoles
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates default roles (Author, Reviewer, Editor, Manager) and assigns permissions."

    def handle(self, *args, **options):
        # contributor and reviewer has no business in admin panel, we only create them
        # to use in the view
        Group.objects.get_or_create(name=UserRoles.CONTRIBUTOR)
        Group.objects.get_or_create(name=UserRoles.REVIEWER)
        editor_group, _ = Group.objects.get_or_create(name=UserRoles.EDITOR)
        manager_group, _ = Group.objects.get_or_create(name=UserRoles.MANAGER)

        u_content_type = ContentType.objects.get_for_model(User)

        user_permissions = Permission.objects.filter(content_type=u_content_type)

        editor_perms = ["can_view_article", "change_change_article"]
        for perm in editor_perms:
            editor_group.permissions.add(Permission.objects.get(codename=perm))

        manager_group.permissions.add(*user_permissions)

        self.stdout.write(self.style.SUCCESS("Successfully created roles!"))
        self.stdout.write(self.style.SUCCESS("Successfully created roles!"))
