import logging

from apps.accounts.emails import EmailThread
from apps.content.models import Article
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

User = get_user_model()
logger = logging.getLogger(__name__)


class NotificationService:
    """
    Handles all email notifications for subscriptions.
    """

    def __init__(self):
        self.frontend_url = settings.FRONTEND_URL

    def send_email(
        self, subject: str, recipient: str, template_name: str, context: dict
    ) -> bool:
        """
        Send email using Django email backend.

        Args:
            subject: Email subject
            recipient: Recipient email
            template_name: Template file name
            context: Template context

        Returns:
            True if sent successfully
        """
        context.update(
            {
                "frontend_url": self.frontend_url,
            }
        )
        message = render_to_string(template_name, context)
        email_message = EmailMessage(subject=subject, body=message, to=[recipient])
        email_message.content_subtype = "html"
        EmailThread(email_message).start()

    def send_article_submitted_email(self, article, reviewer):
        """Notify reviewer of new assignment"""
        context = {
            "article": article,
            "reviewer": reviewer,
            "review_url": f"{self.frontend_url}/reviews/{article.reviews.get(is_active=True).id}",
        }

        return self.send_email(
            subject=f"New article assigned for review: {article.title}",
            recipient=reviewer.email,
            template_name="content/article_submitted.html",
            context=context,
        )

    def send_review_started_email(self, article):
        """Notify author that review has started"""
        context = {
            "article": article,
            "author": article.author,
            "reviewer": article.assigned_reviewer,
            "article_url": f"{self.frontend_url}/articles/{article.id}/editor",
        }
        self.send_email(
            subject=f"Review started for: {article.title}",
            recipient=article.author.email,
            template_name="content/review_started.html",
            context=context,
        )

    def send_changes_requested_email(self, article):
        """Notify author that changes are requested"""
        context = {
            "article": article,
            "author": article.author,
            "reviewer": article.assigned_reviewer,
            "article_url": f"{self.frontend_url}/articles/{article.id}/editor",
        }
        self.send_email(
            subject=f"Changes requested for: {article.title}",
            recipient=article.author.email,
            template_name="content/changes_requested.html",
            context=context,
        )

    def send_article_approved_email(self, article):
        """Notify author and editor that article is approved"""
        article_url = f"{self.frontend_url}/articles/{article.id}/editor"
        # To author
        author_context = {
            "article": article,
            "author": article.author,
            "reviewer": article.assigned_reviewer,
            "article_url": article_url,
        }
        self.send_email(
            subject=f"Great news! Your article has been approved: {article.title}",
            recipient=article.author.email,
            template_name="content/article_approved_author.html",
            context=author_context,
        )

        # To editor
        if article.assigned_editor:
            editor_context = {
                "article": article,
                "editor": article.assigned_editor,
                "article_url": article_url,
            }
            self.send_email(
                subject=f"New article ready for publishing: {article.title}",
                recipient=article.assigned_editor.email,
                template_name="content/article_approved_editor.html",
                context=editor_context,
            )
        else:
            logger.warning(f"No editor assigned for approved article {article.id}")

    def send_article_rejected_email(self, article):
        """Notify author that article is rejected"""
        context = {
            "article": article,
            "author": article.author,
            "reviewer": article.assigned_reviewer,
            "article_url": f"{self.frontend_url}/articles/{article.id}/editor",
        }
        self.send_email(
            subject=f"Article not approved: {article.title}",
            recipient=article.author.email,
            template_name="content/article_rejected.html",
            context=context,
        )

    def send_article_published_email(self, article):
        """Notify author and reviewer that article is published"""
        published_url = (
            f"{self.frontend_url}/articles/{article.author.username}/{article.slug}"
        )

        # To author
        author_context = {"article": article, "published_url": published_url}
        self.send_email(
            subject=f"🎉 Your article is now published: {article.title}",
            recipient=article.author.email,
            template_name="content/article_published_author.html",
            context=author_context,
        )

        # To reviewer
        review = article.reviews.filter(is_active=True).first()
        if review and review.reviewed_by:
            reviewer_context = {
                "article": article,
                "reviewer": review.reviewed_by,
                "published_url": published_url,
            }
            self.send_email(
                subject=f"Article you reviewed is now published: {article.title}",
                recipient=review.reviewed_by.email,
                template_name="content/article_published_reviewer.html",
                context=reviewer_context,
            )

    def send_reviewer_reassigned_email(self, article, new_reviewer, old_reviewer=None):
        """Notify new reviewer of assignment"""
        context = {
            "article": article,
            "new_reviewer": new_reviewer,
            "old_reviewer": old_reviewer,
            "article_url": f"{self.frontend_url}/articles/{article.id}/editor",
        }

        self.send_email(
            subject=f"Article assigned to you for review: {article.title}",
            recipient=new_reviewer.email,
            template_name="content/reviewer_reassigned.html",
            context=context,
        )

    def send_editor_reassigned_email(self, article, new_editor, old_editor=None):
        """Notify new editor of assignment"""
        context = {
            "article": article,
            "new_editor": new_editor,
            "old_editor": old_editor,
            "article_url": f"{self.frontend_url}/articles/{article.id}/editor",
        }

        self.send_email(
            subject=f"Article assigned to you for publishing: {article.title}",
            recipient=new_editor.email,
            template_name="content/editor_reassigned.html",
            context=context,
        )

    # ThreadNotification
    def send_thread_notification_email(self, webhook_data):
        """
        Notify user about comment/reply activity
        Triggered by Liveblocks Thread webhook
        """
        try:
            data = webhook_data.get("data", {})
            room_id = data.get("roomId", "")
            user_id = data.get("userId", "")
            thread_id = data.get("threadId", "")

            if not room_id.startswith("article-"):
                logger.warning(f"Invalid room_id format: {room_id}")
                return False

            # (e.g., "article-123" -> "123")
            article_id = room_id.replace("article-", "")

            # (remove "user-" prefix if present)
            notified_user_id = user_id.replace("user-", "")

            article = Article.objects.get(id=article_id)
            notified_user = User.objects.get(id=notified_user_id)

            context = {
                "article": article,
                "notified_user": notified_user,
                "thread_id": thread_id,
                "article_url": f"{self.frontend_url}/articles/{article.id}/editor",
            }

            self.send_email(
                subject=f'New activity on "{article.title}"',
                recipient=notified_user.email,
                template_name="content/thread_notification.html",
                context=context,
            )

            logger.info(f"Sent thread notification to {notified_user.email}")
            return True
        except Article.DoesNotExist:
            logger.error(f"Article not found for room_id: {room_id}")
            return False
        except User.DoesNotExist:
            logger.error(f"User not found with id: {notified_user_id}")
            return False
        except Exception as e:
            logger.error(f"Error sending thread notification: {str(e)}")
            return False

    def send_assignment_failure_alert(
        self, article, is_reviewer_missing=False, is_editor_missing=False
    ):
        """
        Alert admins when article submission doesn't have a reviewer or editor assigned.

        Args:
            article: The Article instance
            is_reviewer_missing: True if no reviewer was available
            is_editor_missing: True if no editor was available
        """
        missing_roles = []
        if is_reviewer_missing:
            missing_roles.append("Reviewer")
        if is_editor_missing:
            missing_roles.append("Editor")

        missing_text = " and ".join(missing_roles)

        admin_emails = list(
            User.objects.filter(groups__name="Admin")
            .values_list("email", flat=True)
            .distinct()
        )

        if not admin_emails:
            logger.error(
                f"CRITICAL: No admins found to alert about article {article.id} assignment failure!"
            )
            return False

        context = {
            "article": article,
            "author": article.author,
            "missing_roles": missing_text,
            "is_reviewer_missing": is_reviewer_missing,
            "is_editor_missing": is_editor_missing,
            "admin_dashboard_url": f"{self.frontend_url}/admin/content/article/{article.id}/change/",
            "article_url": f"{self.frontend_url}/articles/{article.id}/editor",
        }

        subject = f"🚨 URGENT: Article Awaiting Manual Assignment - {article.title}"

        for admin_email in admin_emails:
            try:
                self.send_email(
                    subject=subject,
                    recipient=admin_email,
                    template_name="content/assignment_failure_alert.html",
                    context=context,
                )
            except Exception as e:
                logger.error(
                    f"Failed to send assignment alert to {admin_email}: {str(e)}"
                )
                return False

        logger.info(
            f"Sent assignment failure alert for article {article.id} to {len(admin_emails)} admins"
        )
        return True

    def send_author_first_reminder_email(self, article):
        """
        Send first reminder to author about pending revisions.
        Triggered when article is in changes_requested for 20 days.
        """
        context = {
            "article": article,
            "author": article.author,
            "article_url": f"{self.frontend_url}/articles/{article.id}/editor",
        }

        return self.send_email(
            subject=f"Reminder: Your Article Awaiting Revisions - {article.title}",
            recipient=article.author.email,
            template_name="content/author_first_reminder.html",
            context=context,
        )

    def send_author_final_warning_email(self, article):
        """
        Send final warning to author before auto-archiving article.
        Triggered when article is in changes_requested for 45 days.
        """
        context = {
            "article": article,
            "author": article.author,
            "days_remaining": 15,  # 60 - 45 = 15 days left
            "article_url": f"{self.frontend_url}/articles/{article.id}/editor",
        }

        return self.send_email(
            subject=f"Action Required: Your TechHive Article - {article.title}",
            recipient=article.author.email,
            template_name="content/author_final_warning.html",
            context=context,
        )

    def send_author_archived_email(self, article):
        """
        Notify author that their article has been auto-archived due to inactivity.
        Triggered when article is in changes_requested for 60 days.
        """
        context = {
            "article": article,
            "author": article.author,
            "dashboard_url": f"{self.frontend_url}/dashboard/articles",
        }

        return self.send_email(
            subject=f"Article Archived Due to Inactivity - {article.title}",
            recipient=article.author.email,
            template_name="content/author_archived.html",
            context=context,
        )

    def send_reviewer_reminder_email(self, article):
        """
        Send reminder to reviewer about pending review.
        Triggered when article is in submitted_for_review/under_review for 5 days.
        """
        context = {
            "article": article,
            "reviewer": article.assigned_reviewer,
            "author": article.author,
            "review_url": f"{self.frontend_url}/reviews/{article.reviews.filter(completed_at__isnull=True).first().id}",
        }

        return self.send_email(
            subject=f"Reminder: Article Awaiting Your Review - {article.title}",
            recipient=article.assigned_reviewer.email,
            template_name="content/reviewer_reminder.html",
            context=context,
        )

    def send_editor_reminder_email(self, article):
        """
        Send reminder to editor about article ready for publishing.
        Triggered when article is in ready_for_publishing for 7 days.
        """
        context = {
            "article": article,
            "editor": article.assigned_editor,
            "author": article.author,
            "reviewer": article.assigned_reviewer,
            "days_waiting": 7,
            "admin_dashboard_url": f"{self.frontend_url}/admin/content/article/{article.id}/change/",
        }

        return self.send_email(
            subject=f"Reminder: Article Ready for Publishing - {article.title}",
            recipient=article.assigned_editor.email,
            template_name="content/editor_reminder.html",
            context=context,
        )

    def send_editor_escalation_for_stale_review(self, article):
        """
        Alert editor about stale review that needs attention.
        Triggered when article is in submitted_for_review/under_review for 10 days.
        """
        context = {
            "article": article,
            "editor": article.assigned_editor,
            "reviewer": article.assigned_reviewer,
            "days_overdue": 10,
            "admin_dashboard_url": f"{self.frontend_url}/admin/content/article/{article.id}/change/",
            "article_url": f"{self.frontend_url}/articles/{article.id}/editor",
        }

        return self.send_email(
            subject=f"ACTION NEEDED: Stale Review for '{article.title}'",
            recipient=article.assigned_editor.email,
            template_name="content/editor_escalation_stale_review.html",
            context=context,
        )

    def send_admin_escalation_for_stale_publication(self, article):
        """
        Alert admins about article stuck in ready_for_publishing.
        Triggered when article is in ready_for_publishing for 14 days.
        """

        admin_emails = list(
            User.objects.filter(groups__name="Admin")
            .values_list("email", flat=True)
            .distinct()
        )

        if not admin_emails:
            logger.error(
                f"CRITICAL: No admins found to alert about stale publication for article {article.id}!"
            )
            return False

        context = {
            "article": article,
            "editor": article.assigned_editor,
            "days_waiting": 14,
            "admin_dashboard_url": f"{self.frontend_url}/admin/content/article/{article.id}/change/",
            "article_url": f"{self.frontend_url}/articles/{article.id}/editor",
        }

        subject = f"ESCALATION: Stale Article Ready for Publishing - {article.title}"

        for admin_email in admin_emails:
            try:
                self.send_email(
                    subject=subject,
                    recipient=admin_email,
                    template_name="content/admin_escalation_stale_publication.html",
                    context=context,
                )
            except Exception as e:
                logger.error(
                    f"Failed to send stale publication escalation to {admin_email}: {str(e)}"
                )

        logger.info(
            f"Sent stale publication escalation for article {article.id} to {len(admin_emails)} admins"
        )
        return True


notification_service = NotificationService()


# Can This Scenario Even Happen?
# The good news: Liveblocks is smart enough to prevent this scenario on their end.
# "The event won't be triggered if the user has seen the thread..."

# When Alice mentions herself (e.g., types @Alice test), she immediately "sees" the thread because she's the one who created it. Therefore, Liveblocks will never send a webhook notification to Alice about her own comment.

# Liveblocks handles this edge case for you automatically.

# According to the Liveblocks documentation:

# "The event won't be triggered if the user has seen the thread..."
# TODO: MOST OF THE article_url are non-existent so fix that in the frontend
