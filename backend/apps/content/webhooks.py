import hashlib
import hmac
import json
import logging
from datetime import timezone

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from backend.apps.content import notification_service
from backend.apps.content.models import LiveblocksWebhookEvent
from backend.apps.content.utils import handle_storage_updated

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def liveblocks_webhook(request):
    """Handle Liveblocks webhook events"""

    signature = request.headers.get("X-Liveblocks-Signature")
    webhook_secret = settings.LIVEBLOCKS_WEBHOOK_SECRET

    expected_signature = hmac.new(
        webhook_secret.encode("utf-8"), request.body, hashlib.sha256
    ).hexdigest()

    is_valid = hmac.compare_digest(expected_signature, signature)
    if not is_valid:
        logger.warning("Invalid webhook signature detected")
        return HttpResponse(status=400)

    try:
        webhook_data = json.loads(request.body.decode("utf-8"))
    except ValueError:
        logger.exception("Invalid JSON payload")
        return HttpResponse(status=400)

    event_type = webhook_data.get("type")

    webhook_event = LiveblocksWebhookEvent.objects.create(
        event_type=event_type,
        room_id=webhook_data.get("data", {}).get("roomId", ""),
        payload=webhook_data,
    )

    try:
        if event_type == "storageUpdated":
            handle_storage_updated(webhook_data, webhook_event)

        elif event_type == "notification":
            notification_kind = webhook_data.get("data", {}).get("kind")

            # ONLY handle thread notifications
            if notification_kind == "thread":

                notification_service.send_thread_notification_email(webhook_data)

        webhook_event.processed = True
        webhook_event.processed_at = timezone.now()
        webhook_event.save()

    except Exception as e:
        webhook_event.error_message = str(e)
        webhook_event.save()

    return HttpResponse(status=200)

