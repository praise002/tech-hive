import uuid

from apps.common.models import BaseModel
from apps.common.validators import validate_file_size
from apps.content.choices import ArticleReviewStatusChoices, ArticleStatusChoices
from apps.content.manager import (
    ActiveManager,
    PublishedManager,
    SavedPublishedArticlesManager,
)
from apps.content.utils import ReadabilityMetrics
from autoslug import AutoSlugField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.db.models import Count
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


class Tag(BaseModel):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def clean(self):  # called automatically when saving forms/admin
        if self.name:
            self.name = self.name.lower()

    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from="name", unique=True, always_update=True)
    desc = models.TextField()

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Article(BaseModel):
    category = models.ForeignKey(
        Category,
        related_name="articles",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    content = CKEditor5Field("Article Content", config_name="extends")
    cover_image = models.ImageField(
        upload_to="articles/", null=True, blank=True, validators=[validate_file_size]
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="articles")
    status = models.CharField(
        max_length=20,
        choices=ArticleStatusChoices.choices,
        default=ArticleStatusChoices.DRAFT,
    )
    is_featured = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_articles",
    )
    # Workflow Assignment
    assigned_reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_reviews",
    )

    assigned_editor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_edits",
    )

    # Liveblocks Sync Tracking
    content_last_synced_at = models.DateTimeField(
        null=True, blank=True, help_text="Last time content was synced from Liveblocks"
    )

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def clean(self):
        if self.tags.count() > 5:
            raise ValidationError("Maximum 5 tags allowed per article")

        if self.published_at and self.status != ArticleStatusChoices.PUBLISHED:
            raise ValidationError(
                "Published date can only be set when article status is 'Published'"
            )

        if self.status != ArticleStatusChoices.PUBLISHED and self.is_featured:
            raise ValidationError(
                "'Is featured' can only be set when article status is 'Published'"
            )

    def calculate_read_time(self):
        return ReadabilityMetrics.method_hybrid(self.content)

    @property
    def cover_image_url(self):
        try:
            url = self.cover_image.url
        except:
            url = ""
        return url

    # NOTE: IF THESE BECOMES A PERFORMANCE ISSUE CACHE THE COUNT
    @property
    def total_reaction_counts(self):
        return self.reactions.count()

    @property
    def reaction_counts(self):
        """
        Returns a dict like {'❤️': 5, '👍': 2, ...} for this article.
        """
        counts = self.reactions.values("reaction_type").annotate(count=Count("id"))
        return {item["reaction_type"]: item["count"] for item in counts}

    @property
    def all_comments_count(self):
        """Total active comments on this article"""
        return self.comments.filter(is_active=True).count()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-title"]),
            models.Index(fields=["assigned_reviewer", "status"]),
            models.Index(fields=["assigned_editor", "status"]),
            models.Index(fields=["status", "-created_at"]),
        ]


class ArticleReaction(BaseModel):
    EMOJI_CHOICES = [
        ("❤️", "Heart"),
        ("😍", "Heart Eyes"),
        ("👍", "Thumbs Up"),
        ("🔥", "Fire"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="reactions"
    )
    reaction_type = models.CharField(max_length=20, choices=EMOJI_CHOICES)

    class Meta:
        unique_together = ("user", "article", "reaction_type")

    def __str__(self):
        return f"{self.user} {self.reaction_type} {self.article}"


class SavedArticle(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="saved_articles",
    )
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="saved_by_user"
    )
    saved_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    published = SavedPublishedArticlesManager()

    class Meta:
        unique_together = ("article", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return self.article.title


class ArticleReview(BaseModel):

    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="reviews"
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="article_reviews",
        on_delete=models.CASCADE,
    )

    status = models.CharField(
        max_length=20,
        choices=ArticleReviewStatusChoices.choices,
        default=ArticleReviewStatusChoices.PENDING,
    )

    updated_at = models.DateTimeField(auto_now=True)

    started_at = models.DateTimeField(
        null=True, blank=True, help_text="When reviewer started the review"
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When review was completed (approved/rejected/changes requested)",
    )

    reviewer_notes = models.TextField(
        null=True, blank=True, help_text="Private notes for reviewer's reference only"
    )

    objects = models.Manager()

    class Meta:
        # NOTE: NO UNIQUE CONSTRIANT
        # unique_together = ("article", "is_active")
        indexes = [
            models.Index(fields=["article", "status"]),
            models.Index(fields=["reviewed_by", "status"]),
        ]

    def __str__(self):
        return f"Review of {self.article} by {self.reviewed_by}"


# Submit Article for Review
class ArticleWorkflowHistory(BaseModel):
    """Audit trail for article status changes"""

    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="workflow_history"
    )

    from_status = models.CharField(max_length=20, choices=ArticleStatusChoices.choices)

    to_status = models.CharField(max_length=20, choices=ArticleStatusChoices.choices)

    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="status_changes",
    )

    changed_at = models.DateTimeField(auto_now_add=True)

    notes = models.TextField(
        null=True, blank=True, help_text="Optional notes about the status change"
    )

    class Meta:
        ordering = ["-changed_at"]
        indexes = [
            models.Index(fields=["article", "-changed_at"]),
        ]
        verbose_name_plural = "Article Workflow Histories"

    def __str__(self):
        return f"{self.article.title}: {self.from_status} → {self.to_status}"


class LiveblocksWebhookEvent(BaseModel):
    """Log all Liveblocks webhook events for debugging"""

    event_type = models.CharField(
        max_length=50,
        help_text="Type of webhook event (storageUpdated, notificationEvent, etc.)",
    )

    room_id = models.CharField(
        max_length=100, help_text="Liveblocks room ID (e.g., article-123)"
    )

    payload = models.JSONField(help_text="Full webhook payload")

    processed = models.BooleanField(
        default=False, help_text="Whether the event was successfully processed"
    )

    processed_at = models.DateTimeField(null=True, blank=True)

    error_message = models.TextField(
        null=True, blank=True, help_text="Error message if processing failed"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["room_id", "-created_at"]),
            models.Index(fields=["processed", "-created_at"]),
            models.Index(fields=["event_type", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.event_type} - {self.room_id} at {self.created_at}"


class CommentThread(BaseModel):
    """
    Represents a conversation thread tied to an article.
    Each root comment starts a new thread, all replies go to the same thread.
    """

    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comment_threads"
    )
    # The very first comment that started this thread
    root_comment = models.OneToOneField(
        "Comment", on_delete=models.CASCADE, related_name="thread_root"
    )
    is_active = models.BooleanField(default=True)
    reply_count = models.IntegerField(default=0)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        indexes = [
            models.Index(fields=["article", "is_active"]),
        ]

    def __str__(self):
        return f"Thread for {self.article.title} - {self.reply_count} replies"


class Comment(BaseModel):
    thread = models.ForeignKey(
        CommentThread,
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True,
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="comments",
    )  # denormalization
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments_by_user",
    )
    body = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)  # for moderation purposes

    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["thread", "-created_at"]),
        ]

    def __str__(self):
        # if self.replying_to:
        #     return f"{self.user.full_name} → @{self.replying_to.username}: {self.body[:30]}..."
        return f"{self.user.full_name}: {self.body[:40]}..."

    @property
    def is_root_comment(self):
        """Check if this comment is the root of its thread"""
        return self.thread_id and self.thread.root_comment_id == self.id

    def get_all_replies_count(self):
        """
        Get reply count ONLY for root comments.
        Non-root comments return 0.
        """
        if self.is_root_comment:
            return self.thread.reply_count
        return 0


class CommentMention(BaseModel):
    """Track who was mentioned in a comment"""

    comment = models.ForeignKey(
        Comment, related_name="mentions", on_delete=models.CASCADE
    )
    mentioned_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_mentions",
        on_delete=models.SET_NULL,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("comment", "mentioned_user")
        indexes = [
            models.Index(fields=["mentioned_user"]),
        ]


class Job(BaseModel):
    JOB_TYPE_CHOICES = [
        ("FULL_TIME", "Full-time"),
        ("PART_TIME", "Part-time"),
        ("CONTRACT", "Contract"),
    ]
    WORK_MODE_CHOICES = [
        ("REMOTE", "Remote"),
        ("HYBRID", "Hybrid"),
        ("ONSITE", "Onsite"),
    ]
    category = models.ForeignKey(
        Category, related_name="jobs", on_delete=models.SET_NULL, null=True
    )
    title = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    company = models.CharField(max_length=250)
    desc = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    url = models.CharField(max_length=250, validators=[URLValidator()])
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    job_type = models.CharField(
        max_length=20, choices=JOB_TYPE_CHOICES, default="FULL_TIME"
    )
    work_mode = models.CharField(
        max_length=20, choices=WORK_MODE_CHOICES, default="ONSITE"
    )
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Event(BaseModel):
    category = models.ForeignKey(
        Category, related_name="events", on_delete=models.SET_NULL, null=True
    )
    title = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    desc = models.TextField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=100)
    agenda = models.TextField()
    ticket_url = models.CharField(max_length=250, validators=[URLValidator()])

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Resource(BaseModel):
    category = models.ForeignKey(
        Category, related_name="resources", on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from="name", unique=True, always_update=True)
    image = models.ImageField(
        upload_to="resources/", null=True, blank=True, validators=[validate_file_size]
    )
    body = models.TextField()
    url = models.CharField(max_length=250, validators=[URLValidator()])
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url

    def __str__(self):
        return self.name


class ToolTag(BaseModel):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Tool(BaseModel):
    category = models.ForeignKey(
        Category, related_name="tools", on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from="name", unique=True, always_update=True)
    desc = models.TextField()
    url = models.CharField(max_length=250, validators=[URLValidator()])
    image_url = models.CharField(max_length=250, validators=[URLValidator()])
    tags = models.ManyToManyField(ToolTag)
    call_to_action = models.CharField(
        max_length=100,
        default="Explore",
        help_text="Dynamic button text (e.g., 'Sign Up to GitHub', 'Try Figma for Free')",
    )
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
