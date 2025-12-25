from apps.content.choices import ArticleStatusChoices
from django.db import models


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=ArticleStatusChoices.PUBLISHED)


class SavedPublishedArticlesManager(models.Manager):
    """Manager that returns only saved articles where the article is published."""

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(article__status=ArticleStatusChoices.PUBLISHED)
        )


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
