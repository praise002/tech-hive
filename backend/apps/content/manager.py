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


class ContentManager(models.Manager):
    """Manager for content models (Job, Event, Resource, Tool) with active() and published() methods"""

    def active(self):
        return self.filter(is_active=True)

    def published(self):
        return self.filter(is_published=True)
