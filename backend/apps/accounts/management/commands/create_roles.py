# yourapp/management/commands/create_roles.py
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from apps.accounts.utils import UserRoles
from apps.content.models import Article


class Command(BaseCommand):
    help = "Creates default roles (Author, Reviewer, Editor, Manager) and assigns permissions."

    def handle(self, *args, **options):
        contributor_group, _ = Group.objects.get_or_create(name=UserRoles.CONTRIBUTOR)
        reviewer_group, _ = Group.objects.get_or_create(name=UserRoles.REVIEWER)
        editor_group, _ = Group.objects.get_or_create(name=UserRoles.EDITOR)
        manager_group, _ = Group.objects.get_or_create(name=UserRoles.MANAGER)

        content_type = ContentType.objects.get_for_model(Article)
        article_permission = Permission.objects.filter(content_type=content_type)
        # TODO: CONTINUE FOR OTHER MODELS
        
        for perm in article_permission:
            if perm.codename == "delete_post":
                pass

            elif perm.codename == "change_post":
                contributor_group.permissions.add(perm)
                reviewer_group.permissions.add(perm)
                editor_group.permissions.add(perm)
            else:
                contributor_group.permissions.add(perm)
                reviewer_group.permissions.add(perm)
                editor_group.permissions.add(perm)
                manager_group.permissions.add(perm)
        
        contributor_perms = [
            
        ]
        for perm in contributor_perms:
            contributor_group.permissions.add(Permission.objects.get(codename=perm))
            
        reviewer_perms = [
            
        ]
        for perm in reviewer_perms:
            reviewer_group.permissions.add(Permission.objects.get(codename=perm))


        editor_perms = [
            
        ]
        for perm in editor_perms:
            editor_group.permissions.add(Permission.objects.get(codename=perm))

        # TODO: is_staff=True so can access admin panel
        # give additional permissions form the admin panel
        manager_perms = [
            
        ]
        for perm in manager_perms:
            manager_group.permissions.add(Permission.objects.get(codename=perm))

        self.stdout.write(self.style.SUCCESS("Successfully created roles!"))
