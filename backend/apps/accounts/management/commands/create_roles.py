from apps.accounts.models import User
from apps.accounts.utils import UserRoles
from apps.content.models import Article, ArticleReview, Category, Tag
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates default roles (Author, Reviewer, Editor, Manager) and assigns permissions."

    def handle(self, *args, **options):

        Group.objects.get_or_create(name=UserRoles.CONTRIBUTOR)
        Group.objects.get_or_create(name=UserRoles.REVIEWER)
        editor_group, _ = Group.objects.get_or_create(name=UserRoles.EDITOR)
        manager_group, _ = Group.objects.get_or_create(name=UserRoles.MANAGER)

        user_ct = ContentType.objects.get_for_model(User)
        article_ct = ContentType.objects.get_for_model(Article)
        category_ct = ContentType.objects.get_for_model(Category)
        tag_ct = ContentType.objects.get_for_model(Tag)
        article_review_ct = ContentType.objects.get_for_model(ArticleReview)

        editor_perms_config = [
            ("view_article", article_ct),
            ("change_article", article_ct),
            ("add_category", category_ct),
            ("change_category", category_ct),
            ("delete_category", category_ct),
            ("view_category", category_ct),
            ("add_tag", tag_ct),
            ("change_tag", tag_ct),
            ("delete_tag", tag_ct),
            ("view_tag", tag_ct),
        ]

        self._assign_permissions(editor_group, editor_perms_config, "Editor")

        manager_perms_config = [
            ("add_user", user_ct),
            ("change_user", user_ct),
            ("delete_user", user_ct),
            ("view_user", user_ct),
            ("change_article", article_ct),
            ("view_article", article_ct),
            ("add_articlereview", article_review_ct),
            ("change_articlereview", article_review_ct),
            ("delete_articlereview", article_review_ct),
            ("view_articlereview", article_review_ct),
        ]

        self._assign_permissions(manager_group, manager_perms_config, "Manager")

        self.stdout.write(self.style.SUCCESS("\nSuccessfully created roles!"))

    def _assign_permissions(self, group, perms_config, group_name):
        """Helper method to assign permissions with error handling"""
        for codename, content_type in perms_config:
            try:
                perm = Permission.objects.get(
                    codename=codename, content_type=content_type
                )
                group.permissions.add(perm)
                self.stdout.write(f"✓ Added '{codename}' to {group_name}")
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"✗ Permission '{codename}' for {content_type.model} does not exist"
                    )
                )
