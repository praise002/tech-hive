from datetime import timedelta

from apps.content.models import Article, ArticleStatusChoices
from celery import shared_task
from django.utils import timezone

from . import notification_service


@shared_task(name="process_stale_workflows")
def process_stale_workflows():
    """
    A daily task to handle inactive articles in the review and publishing pipeline.
    - Reminds authors to resubmit changes.
    - Archives abandoned articles.
    - Reminds reviewers of pending reviews and escalates to editors.
    - Reminds editors of pending publications and escalates to managers.
    """
    handle_author_inactivity()
    handle_reviewer_inactivity()
    handle_editor_inactivity()


def handle_author_inactivity():
    """
    Handles articles stuck in 'CHANGES_REQUESTED'.
    - Day 20: Reminder
    - Day 45: Final Warning
    - Day 60: Auto-Archive
    """
    # Auto-Archive (Day 60)
    archive_date = timezone.now() - timedelta(days=60)
    articles_to_archive = Article.objects.filter(
        status=ArticleStatusChoices.CHANGES_REQUESTED, updated_at__lt=archive_date
    )
    for article in articles_to_archive:
        article.status = ArticleStatusChoices.DRAFT  # Move back to draft
        article.save(update_fields=["status", "updated_at"])
        notification_service.send_author_archived_email(article)

    # Final Warning (Day 45)
    warning_date = timezone.now() - timedelta(days=45)
    final_warning_articles = Article.objects.filter(
        status=ArticleStatusChoices.CHANGES_REQUESTED,
        updated_at__lt=warning_date,
        updated_at__gte=archive_date,  # Avoid sending to already processed articles
    )
    for article in final_warning_articles:
        notification_service.send_author_final_warning_email(article)

    # First Reminder (Day 20)
    first_reminder_date = timezone.now() - timedelta(days=20)
    first_reminder_articles = Article.objects.filter(
        status=ArticleStatusChoices.CHANGES_REQUESTED,
        updated_at__lt=first_reminder_date,
        updated_at__gte=warning_date,  # Between Day 20 and Day 45 (not yet warned)
    )
    for article in first_reminder_articles:
        notification_service.send_author_first_reminder_email(article)


def handle_reviewer_inactivity():
    """
    Handles articles stuck in 'SUBMITTED_FOR_REVIEW' or 'UNDER_REVIEW'.
    - Day 5: Reviewer Reminder
    - Day 10: Escalation to Editor
    """
    # Escalation to Editor (Day 10)
    escalation_date = timezone.now() - timedelta(days=10)
    reviews_to_escalate = Article.objects.filter(
        status__in=[
            ArticleStatusChoices.SUBMITTED_FOR_REVIEW,
            ArticleStatusChoices.UNDER_REVIEW,
        ],
        updated_at__lt=escalation_date,
    ).select_related("assigned_reviewer", "assigned_editor")
    for article in reviews_to_escalate:
        if article.assigned_editor:
            notification_service.send_editor_escalation_for_stale_review(article)

    # Reviewer Reminder (Day 5)
    reminder_date = timezone.now() - timedelta(days=5)
    reviews_to_remind = Article.objects.filter(
        status__in=[
            ArticleStatusChoices.SUBMITTED_FOR_REVIEW,
            ArticleStatusChoices.UNDER_REVIEW,
        ],
        updated_at__lt=reminder_date,
        updated_at__gte=escalation_date,
    ).select_related("assigned_reviewer")
    for article in reviews_to_remind:
        notification_service.send_reviewer_reminder_email(article)


def handle_editor_inactivity():
    """
    Handles articles stuck in 'READY_FOR_PUBLISHING'.
    - Day 7: Editor Reminder
    - Day 14: Escalation to Manager/Admin
    """
    # Escalation to Admin(Day 14)
    admin_escalation_date = timezone.now() - timedelta(days=14)
    articles_to_escalate = Article.objects.filter(
        status=ArticleStatusChoices.READY, updated_at__lt=admin_escalation_date
    ).select_related("assigned_editor")
    for article in articles_to_escalate:
        notification_service.send_manager_escalation_for_stale_publication(article)
