from apps.content import models
from django.contrib import admin

from backend.apps.accounts.models import ContributorOnboarding

@admin.register(ContributorOnboarding)
class ContributorOnboardingAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ArticleReaction)
class ArticleReactionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ArticleReview)
class ArticleReview(admin.ModelAdmin):
    pass


@admin.register(models.SavedArticle)
class SavedArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Resource)
class ResourceAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ToolTag)
class ToolTagAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Tool)
class ToolAdmin(admin.ModelAdmin):
    pass
