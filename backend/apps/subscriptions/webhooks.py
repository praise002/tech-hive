import json
import logging

from apps.subscriptions.services import webhook_service
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)


@require_POST
@csrf_exempt
def webhook(request):
    try:
        signature = request.headers.get("x-paystack-signature")

        if not signature:
            logger.error("Webhook received without signature")
            return HttpResponse(status=400)

        raw_body = request.body
        # payload = request.data
        # payload = raw_body.get("data", {})
        
        try:
            payload = json.loads(raw_body) if raw_body else {}
        except json.JSONDecodeError:
            logger.error("Webhook received with invalid JSON")
            return HttpResponse(status=400)
            
        event_type = payload.get("event")

        if not event_type:
            logger.error("Webhook received without event type")
            return HttpResponse(status=400)

        logger.info(f"Webhook received: {event_type}")

        success = webhook_service.process_webhook(
            event_type=event_type,
            payload=payload,
            signature=signature,
            raw_body=raw_body,
        )

        if success:
            logger.info("Webhook processed successfully")
            return HttpResponse(status=200)
        else:
            logger.info("Webhook processing failed")
            return HttpResponse(status=400)

    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return HttpResponse(status=500)
