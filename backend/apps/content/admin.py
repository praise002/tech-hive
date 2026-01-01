from apps.accounts.utils import UserRoles
from apps.content import models
from apps.content.choices import ArticleStatusChoices
from django.contrib import admin


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "articles_count", "created_at"]
    search_fields = ["name"]
    readonly_fields = ["id", "slug", "created_at"]

    def articles_count(self, obj):
        return obj.articles.count()

    articles_count.short_description = "Articles"


class UnassignedFilter(admin.SimpleListFilter):
    title = "Unassigned Reviewer/Editor"
    parameter_name = "unassigned"

    def lookups(self, request, model_admin):
        return (("unassigned", "No Reviewer or Editor Assigned"),)

    def queryset(self, request, queryset):
        if self.value() == "unassigned":
            return queryset.filter(
                status=ArticleStatusChoices.SUBMITTED_FOR_REVIEW,
                assigned_reviewer__isnull=True,
                assigned_editor__isnull=True,
            )
        return queryset


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "status",
        "author",
        "category",
        "is_featured",
        "published_at",
        "assigned_reviewer",
        "assigned_editor",
        "content_last_synced_at",
        "get_tags",
    ]
    list_filter = [
        "status",
        "category",
        "is_featured",
        "created_at",
        "assigned_reviewer",
        "assigned_editor",
        UnassignedFilter,
    ]
    search_fields = ["title", "author__email", "author__first_name"]
    filter_horizontal = ["tags"]
    readonly_fields = [
        "id",
        "slug",
        "created_at",
        "updated_at",
        "cover_image_url",
        "content_last_synced_at",
    ]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("title", "slug", "author", "category", "content")},
        ),
        ("Media", {"fields": ("cover_image", "cover_image_url")}),
        ("Classification", {"fields": ("tags", "status", "is_featured")}),
        (
            "Dates",
            {
                "fields": ("published_at", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
        ("Metadata", {"fields": ("id",), "classes": ("collapse",)}),
    )

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()[:3]])

    get_tags.short_description = "Tags"

    def has_change_permission(self, request, obj=None):
        # First, check the default permission
        has_perm = super().has_change_permission(request, obj)
        if not has_perm:
            return False
        
        # Superusers should have full access
        if request.user.is_superuser:
            return True

        # Only allow editors to edit
        if not request.user.groups.filter(name=UserRoles.EDITOR).exists():
            return False

        # If no object, allow (for list view, etc.)
        if obj is None:
            return True

        # Only allow editing if status is PUBLISHED or READY
        return obj.status in ["PUBLISHED", "READY"]


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "articles_count", "created_at"]
    search_fields = ["name"]
    readonly_fields = ["id", "created_at"]

    def articles_count(self, obj):
        return obj.articles.count()

    articles_count.short_description = "Articles"


@admin.register(models.ArticleReaction)
class ArticleReactionAdmin(admin.ModelAdmin):
    list_display = ["user", "article", "reaction_type", "created_at"]
    list_filter = ["reaction_type", "created_at"]
    search_fields = ["user__email", "article__title"]
    readonly_fields = ["id", "created_at"]


@admin.register(models.ArticleReview)
class ArticleReviewAdmin(admin.ModelAdmin):
    list_display = ["article", "reviewed_by", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["article__title", "reviewed_by__email"]
    readonly_fields = ["id", "created_at"]


@admin.register(models.ArticleWorkflowHistory)
class ArticleWorkflowHistoryAdmin(admin.ModelAdmin):
    list_display = [
        "article",
        "from_status",
        "to_status",
        "changed_by",
        "changed_at",
        "notes",
    ]
    list_filter = [
        "from_status",
        "to_status",
        "changed_by",
        "changed_at",
    ]
    search_fields = [
        "article__title",
        "changed_by__email",
        "notes",
    ]
    readonly_fields = [
        "id",
        "article",
        "from_status",
        "to_status",
        "changed_by",
        "changed_at",
        "notes",
        "created_at",
    ]


@admin.register(models.SavedArticle)
class SavedArticleAdmin(admin.ModelAdmin):
    list_display = ["article", "user", "saved_at"]
    list_filter = ["saved_at"]
    search_fields = ["article__title", "user__email"]
    readonly_fields = ["id", "saved_at", "created_at"]


@admin.register(models.CommentThread)
class CommentThreadAdmin(admin.ModelAdmin):
    list_display = ["article", "reply_count", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["article__title"]
    readonly_fields = ["id", "reply_count", "created_at"]


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "article",
        "body_preview",
        "is_root",
        "is_active",
        "created_at",
    ]
    list_filter = ["is_active", "created_at"]
    search_fields = ["body", "user__email", "article__title"]
    readonly_fields = ["id", "created_at", "updated_at"]

    def body_preview(self, obj):
        return obj.body[:50] + "..." if len(obj.body) > 50 else obj.body

    body_preview.short_description = "Comment"

    def is_root(self, obj):
        return "✓" if obj.is_root_comment else "-"

    is_root.short_description = "Root"


@admin.register(models.CommentMention)
class CommentMentionAdmin(admin.ModelAdmin):
    list_display = ["comment", "mentioned_user", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["mentioned_user__email", "comment__body"]
    readonly_fields = ["id", "created_at"]


@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "company",
        "job_type",
        "work_mode",
        "location",
        "is_active",
        "created_at",
    ]
    list_filter = ["job_type", "work_mode", "is_active", "category", "created_at"]
    search_fields = ["title", "company", "location"]
    readonly_fields = ["id", "created_at"]


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "location",
        "start_date",
        "end_date",
        "category",
        "created_at",
    ]
    list_filter = ["category", "start_date", "created_at"]
    search_fields = ["title", "location"]
    readonly_fields = ["id", "created_at"]


@admin.register(models.Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "is_featured", "created_at"]
    list_filter = ["is_featured", "category", "created_at"]
    search_fields = ["name", "body"]
    readonly_fields = ["id", "image_url", "created_at"]


@admin.register(models.ToolTag)
class ToolTagAdmin(admin.ModelAdmin):
    list_display = ["name", "tools_count", "created_at"]
    search_fields = ["name"]
    readonly_fields = ["id", "created_at"]

    def tools_count(self, obj):
        return obj.tool_set.count()

    tools_count.short_description = "Tools"


@admin.register(models.Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "call_to_action",
        "is_featured",
        "get_tags",
        "created_at",
    ]
    list_filter = ["is_featured", "category", "created_at"]
    search_fields = ["name", "desc"]
    filter_horizontal = ["tags"]
    readonly_fields = ["id", "created_at"]

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()[:3]])

    get_tags.short_description = "Tags"
