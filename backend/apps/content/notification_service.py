import logging

from apps.accounts.emails import EmailThread
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
        }
        # {settings.FRONTEND_URL}/reviews/{article.reviews.get(is_active=True).id}
        return self.send_email(
            subject=f"New article assigned for review: {article.title}",
            recipient=reviewer.email,
            template_name="",
            context=context,
        )

    def send_review_started_email(article):
        """Notify author that review has started"""
        pass

    def send_changes_requested_email(article):
        """Notify author that changes are requested"""
        pass

    def send_article_approved_email(article):
        """Notify author and editor that article is approved"""
        pass

    def send_article_rejected_email(article):
        """Notify author that article is rejected"""
        pass

    def send_article_published_email(article, review):
        """Notify author and reviewer that article is published"""
        pass
    
    # TODO: LISTEN TO THE WEBHOOK - ThreadMention
    def send_mention_notification_email(mentioned_user, article, mentioner):
        """Notify user they were mentioned in Liveblocks comment"""
        pass
    
    # TODO: LISTEN TO THE WEBHOOK - ThreadNotification 
    def send_thread_notification_email(webhook_data):
        """
        Notify relevant users about new comments or replies in threads
        """
        pass
