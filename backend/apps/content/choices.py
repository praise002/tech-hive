from django.db import models

CURSOR_COLORS = [
    "#FF6B6B",
    "#4ECDC4",
    "#45B7D1",
    "#FFA07A",
    "#98D8C8",
    "#F7DC6F",
    "#BB8FCE",
    "#85C1E2",
    "#F8B739",
    "#52B788",
    "#0000FF",
]


class ArticleStatusChoices(models.TextChoices):
    DRAFT = "draft", "Draft"
    SUBMITTED_FOR_REVIEW = "submitted_for_review", "Submitted for Review"
    UNDER_REVIEW = "under_review", "Under Review"
    CHANGES_REQUESTED = "changes_requested", "Changes Requested"
    READY = "ready_for_publishing", "Ready for Publishing"
    PUBLISHED = "published", "Published"
    REJECTED = "rejected", "Rejected"
    # ARCHIVED = "archived", "Archived"


class ArticleReviewStatusChoices(models.TextChoices):
    PENDING = "pending", "Pending Assignment"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
