# yourapp/management/commands/create_roles.py
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates default roles (Author, Editor, Manager) and assigns permissions."

    def handle(self, *args, **options):
        contributor_group, _ = Group.objects.get_or_create(name="Author")
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        manager_group, _ = Group.objects.get_or_create(name="Manager")

        contributor_perms = [
            "can_submit_for_review",
            "can_withdraw_from_review",
        ]
        for perm in contributor_perms:
            contributor_group.permissions.add(Permission.objects.get(codename=perm))

        editor_perms = [
            "can_publish_article",
            "can_request_revisions",
        ]
        for perm in editor_perms:
            editor_group.permissions.add(Permission.objects.get(codename=perm))

        # TODO: is_staff=True so can access admin panel
        # give additional permissions form the admin panel
        manager_perms = [
            "can_archive_techive_article",  # NOTE: TECH HIVE ARTICLE ONLY
            "can_publish_article",
        ]
        for perm in manager_perms:
            manager_group.permissions.add(Permission.objects.get(codename=perm))

        self.stdout.write(self.style.SUCCESS("Successfully created roles!"))
