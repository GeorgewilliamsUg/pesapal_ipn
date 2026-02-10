import json
import os
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@csrf_exempt
def create_order(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        body = request.body.decode("utf-8")
        data = json.loads(body)
    except Exception as e:
        logger.error(f"JSON error: {e}")
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    logger.info(f"Incoming payload: {data}")

    required = ["amount", "currency", "first_name", "last_name", "email"]
    missing = [f for f in required if f not in data]

    if missing:
        return JsonResponse(
            {"error": f"Missing fields: {', '.join(missing)}"},
            status=400
        )

    consumer_key = os.environ.get("PESAPAL_CONSUMER_KEY")
    consumer_secret = os.environ.get("PESAPAL_CONSUMER_SECRET")

    if not consumer_key or not consumer_secret:
        logger.error("PesaPal env vars missing")
        return JsonResponse(
            {"error": "Payment configuration error"},
            status=500
        )

    return JsonResponse({"status": "ok"})
