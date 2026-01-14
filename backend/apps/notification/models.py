from apps.common.models import BaseModel, IsDeletedModel
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Notification(IsDeletedModel, BaseModel):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="acted_notifications",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )  # who performed the action
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_notifications",
        on_delete=models.CASCADE,
    )
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="target_obj",
        on_delete=models.CASCADE,
    )
    target_id = models.CharField(null=True, blank=True)
    target = GenericForeignKey("target_ct", "target_id")
    is_read = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["target_ct", "target_id"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.actor} {self.verb}: {self.recipient}: "
