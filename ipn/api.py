import json
import uuid
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import get_access_token

@csrf_exempt
def create_order(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        payload = json.loads(request.body)

        amount = payload.get("amount")
        currency = payload.get("currency", "USD")
        email = payload.get("email")

        if not amount or not email:
            return JsonResponse({"error": "Invalid data"}, status=400)

        token = get_access_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        merchant_reference = f"NISSI-{uuid.uuid4().hex[:12]}"

        order_payload = {
            "id": merchant_reference,
            "amount": amount,
            "currency": currency,
            "description": "Donation to Nissi Medical Outreach",
            "callback_url": "https://nissimedicaloutreach.org/thank-you.html",
            "notification_id": settings.PESAPAL_IPN_ID,
            "billing_address": {
                "email_address": email,
                "first_name": payload.get("first_name", ""),
                "last_name": payload.get("last_name", "")
            },
        }

        response = requests.post(
            f"{settings.PESAPAL_BASE_URL}/api/Transactions/SubmitOrderRequest",
            json=order_payload,
            headers=headers,
            timeout=15,
        )

        response.raise_for_status()
        data = response.json()

        return JsonResponse({
            "checkout_url": data.get("redirect_url")
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
