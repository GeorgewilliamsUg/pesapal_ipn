import json
import uuid
import logging
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import get_access_token

logger = logging.getLogger(__name__)

@csrf_exempt
def create_order(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        payload = json.loads(request.body.decode("utf-8"))

        amount = payload.get("amount")
        currency = payload.get("currency", "USD")
        email = payload.get("email")
        first_name = payload.get("first_name", "")
        last_name = payload.get("last_name", "")

        if not amount or not email:
            return JsonResponse({"error": "Invalid data"}, status=400)

        amount = float(amount)  # IMPORTANT

        merchant_reference = f"NISSI-{uuid.uuid4().hex[:12]}"

        token = get_access_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        order_payload = {
            "id": merchant_reference,
            "amount": amount,
            "currency": currency,
            "description": "Donation to Nissi Medical Outreach",
            "callback_url": "https://nissimedicaloutreach.org/thank-you.html",
            "notification_id": settings.PESAPAL_IPN_ID,
            "billing_address": {
                "email_address": email,
                "first_name": first_name,
                "last_name": last_name,
            },
        }

        logger.info("Submitting Pesapal order payload: %s", order_payload)

        response = requests.post(
            "https://pay.pesapal.com/v3/api/Transactions/SubmitOrderRequest",
            json=order_payload,
            headers=headers,
            timeout=20,
        )

        logger.info("Pesapal response status: %s", response.status_code)
        logger.info("Pesapal response body: %s", response.text)

        response.raise_for_status()
        data = response.json()

        if "redirect_url" not in data:
            raise Exception(f"Unexpected Pesapal response: {data}")

        return JsonResponse({"checkout_url": data["redirect_url"]})

    except Exception:
        logger.exception("Create order failed")
        return JsonResponse(
            {"error": "Create order failed. Check server logs."},
            status=500
        )
