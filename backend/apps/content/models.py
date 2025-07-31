from apps.common.models import BaseModel
from autoslug import AutoSlugField
from django.conf import settings
from django.core.validators import URLValidator
from django.db import models
from django.db.models import Count
from django.utils import timezone


class Tag(BaseModel):
    name = models.CharField(max_length=20)


class ArticleStatusChoices(models.TextChoices):
    DRAFT = "draft", "Draft"
    SUBMITTED = "submitted", "Submitted"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"


class Category(BaseModel):
    name = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from="name", unique=True, always_update=True)
    desc = models.TextField()
    
    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class Article(BaseModel):
    category = models.ForeignKey(
        Category, related_name="articles", on_delete=models.SET_NULL, null=True
    )
    title = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    content = (
        models.TextField()
    )  # TODO: WOULD USE A TEXTEDITOR WHICH WILL CONTAIN IMAGES
    cover_image = models.ImageField(upload_to="articles/", null=True, blank=True)
    read_time = models.PositiveIntegerField(help_text="Read time in minutes", default=0)
    tags = models.ManyToManyField(Tag)
    status = models.CharField(
        max_length=20,
        choices=ArticleStatusChoices.choices,
        default=ArticleStatusChoices.DRAFT,
    )
    is_featured = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="authored_articles",
    )

    def __str__(self):
        return self.title

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

    # class Meta:
    #     unique_together = ("user", "article", "emoji")

    def __str__(self):
        return self.article.title


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

    def __str__(self):
        return self.article.name


class Comment(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments_by_user",
    )
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.user.name} comments on {self.user.article}"


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
    title = models.CharField(max_length=250)
    company = models.CharField(max_length=250)
    desc = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    url = models.CharField(max_length=250, validators=[URLValidator()])
    salary = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    job_type = models.CharField(
        max_length=20, choices=JOB_TYPE_CHOICES, default="FULL_TIME"
    )
    work_mode = models.CharField(
        max_length=20, choices=WORK_MODE_CHOICES, default="ONSITE"
    )

    def __str__(self):
        return self.title


class Event(BaseModel):
    title = models.CharField(max_length=250)
    desc = models.TextField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=100)
    agenda = models.TextField()
    ticket_url = models.CharField(max_length=250, validators=[URLValidator()])

    def __str__(self):
        return self.title


class Resource(BaseModel):
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to="resources/", null=True, blank=True)
    body = models.TextField()
    url = models.CharField(max_length=250, validators=[URLValidator()])

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

    def __str__(self):
        return self.name
