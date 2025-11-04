from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Notification(models.Model):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="acted_notifications", on_delete=models.CASCADE,
        null=True, blank=True
    )  # who performed the action
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="received_notifications",  on_delete=models.CASCADE
    ) 
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    target_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="target_obj",
        on_delete=models.CASCADE,
    )
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey("target_ct", "target_id")
    is_read = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=["target_ct", "target_id"]),
        ]
        ordering = ["-created"]
        
    def __str__(self):
        return f"{self.actor} {self.verb}: {self.recipient}: "
