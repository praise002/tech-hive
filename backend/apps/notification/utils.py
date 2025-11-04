import datetime

from apps.notification.models import Notification
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


def create_notification(recipient, verb, target=None, actor=None):
    # check for any similar notification made in the last minute
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_notification = Notification.objects.filter(
        actor=actor, recipient=recipient, verb=verb, created__gte=last_minute
    )

    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_notification = similar_notification.filter(
            target_ct=target_ct, target_id=target.id
        )

    if not similar_notification.exists():
        # no existing notifications found
        notification = Notification(
            actor=actor, recipient=recipient, verb=verb, target=target
        )
        notification.save()
        return True

    return False
