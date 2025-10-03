from apps.common.models import BaseModel
from autoslug import AutoSlugField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.db.models import Count
from django.utils import timezone

from backend.apps.content.manager import PublishedManager, SavedPublishedArticlesManager


class Tag(BaseModel):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def clean(self):
        if self.name:
            self.name = self.name.lower()

    def __str__(self):
        return self.name


class ArticleStatusChoices(models.TextChoices):
    DRAFT = "draft", "Draft"
    SUBMITTED_FOR_REVIEW = "submitted_for_review", "Submitted for Review"
    UNDER_REVIEW = "under_review", "Under Review"
    CHANGES_REQUESTED = "changes_requested", "Changes Requested"
    REVIEW_COMPLETED = "review_completed", "Review Completed"
    READY = "ready_for_publishing", "Ready for Publishing"
    PUBLISHED = "published", "Published"
    REJECTED = "rejected", "Rejected"
    # ARCHIVED = "archived", "Archived"


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
    content = (
        models.TextField()
    )  # TODO: WOULD USE A TEXTEDITOR WHICH WILL CONTAIN IMAGES
    cover_image = models.ImageField(upload_to="articles/", null=True, blank=True)
    read_time = models.PositiveIntegerField(help_text="Read time in minutes", default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.CharField(
        max_length=20,
        choices=ArticleStatusChoices.choices,
        default=ArticleStatusChoices.DRAFT,
    )
    is_featured = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_articles",
    )

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def clean(self):
        if self.tags.count() > 5:
            raise ValidationError("Maximum 5 tags allowed per article")

    # TODO:
    def calculate_read_time(content):
        """
        Calculate read time with consideration for:
        - Code blocks (read slower)
        - Images (add time)
        - Lists (read faster)
        """
        pass

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

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-title"]),
        ]
        permissions = [
            ("publish_article", "Can publish article"),
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
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("article", "is_active")

    def __str__(self):
        return f"Review of {self.article} by {self.reviewed_by}"


class Comment(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments_by_user",
    )
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    body = models.CharField(max_length=250)
    active = models.BooleanField(default=True)  # for moderation purposes
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"Comment by {self.user.full_name} on {self.article}"

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)


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

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Event(BaseModel):
    category = models.ForeignKey(
        Category, related_name="events", on_delete=models.SET_NULL, null=True
    )
    title = models.CharField(max_length=250)
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
    image = models.ImageField(upload_to="resources/", null=True, blank=True)
    body = models.TextField()
    url = models.CharField(max_length=250, validators=[URLValidator()])

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
    desc = models.TextField()
    url = models.CharField(max_length=250, validators=[URLValidator()])
    image_url = models.CharField(max_length=250, validators=[URLValidator()])
    tags = models.ManyToManyField(ToolTag)
    call_to_action = models.CharField(
        max_length=100,
        default="Explore",
        help_text="Dynamic button text (e.g., 'Sign Up to GitHub', 'Try Figma for Free')",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
