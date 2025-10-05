from django.db import models


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
