import logging

from apps.accounts.emails import EmailThread
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from backend.apps.content.models import Article

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
            template_name="article_submitted.html",
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
            template_name="review_started.html",
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
            template_name="changes_requested.html",
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
            template_name="article_approved_author.html",
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
                template_name="article_approved_editor.html",
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
            template_name="article_rejected.html",
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
            template_name="article_published_author.html",
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
                template_name="article_published_reviewer.html",
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
            template_name="reviewer_reassigned.html",
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
            template_name="editor_reassigned.html",
            context=context,
        )

    # TODO: LISTEN TO THE WEBHOOK - ThreadNotification
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
                template_name="thread_notification.html",
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


notification_service = NotificationService()

# Can This Scenario Even Happen?
# The good news: Liveblocks is smart enough to prevent this scenario on their end.
# "The event won't be triggered if the user has seen the thread..."

# When Alice mentions herself (e.g., types @Alice test), she immediately "sees" the thread because she's the one who created it. Therefore, Liveblocks will never send a webhook notification to Alice about her own comment.

# Liveblocks handles this edge case for you automatically.

# According to the Liveblocks documentation:

# "The event won't be triggered if the user has seen the thread..."
# TODO: MOST OF THE article_url are non-existent so fix that in the frontend
# TODO: send_changes_requested_email(self, article) and the webhooks email events looks similar
