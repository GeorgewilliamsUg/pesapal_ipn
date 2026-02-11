import uuid
from decimal import Decimal, InvalidOperation

import requests
from django.conf import settings


def get_access_token():
    url = f"{settings.PESAPAL_BASE_URL}/api/Auth/RequestToken"

    payload = {
        "consumer_key": settings.PESAPAL_CONSUMER_KEY,
        "consumer_secret": settings.PESAPAL_CONSUMER_SECRET,
    }

    response = requests.post(url, json=payload, timeout=15)
    response.raise_for_status()

    token = response.json().get("token")
    if not token:
        raise Exception("Invalid Pesapal token response")

    return token

def submit_order(data):
    token = get_access_token()

    url = f"{settings.PESAPAL_BASE_URL}/api/Transactions/SubmitOrderRequest"

    try:
        amount = Decimal(str(data["amount"])).quantize(Decimal("0.01"))
    except (InvalidOperation, KeyError, TypeError) as exc:
        raise ValueError("Invalid amount") from exc

    currency = str(data.get("currency", "")).upper()
    if not currency:
        raise ValueError("Currency is required")

    billing_address = {
        "email_address": data["email"],
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "phone_number": data.get("phone_number", "0700000000"),
        "country_code": data.get("country_code", "UG"),
    }

    # Optional billing fields if provided by the client
    optional_fields = [
        "middle_name",
        "line_1",
        "line_2",
        "city",
        "state",
        "postal_code",
        "zip_code",
    ]
    for field in optional_fields:
        if data.get(field):
            billing_address[field] = data[field]

    callback_url = getattr(
        settings,
        "PESAPAL_CALLBACK_URL",
        "https://nissimedicaloutreach.org/thank-you.html",
    )

    payload = {
        "id": str(uuid.uuid4()),
        "currency": currency,
        "amount": float(amount),
        "description": data.get("description", "Nissi Medical Outreach Donation"),
        "callback_url": callback_url,
        "notification_id": settings.PESAPAL_IPN_ID,
        "billing_address": billing_address,
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers, timeout=15)

    print("Pesapal status:", response.status_code)
    print("Pesapal response:", response.text)

    response.raise_for_status()
    return response.json()


def verify_payment(order_tracking_id):
    if not order_tracking_id:
        raise ValueError("order_tracking_id is required")

    token = get_access_token()

    url = (
        f"{settings.PESAPAL_BASE_URL}/api/Transactions/GetTransactionStatus"
        f"?orderTrackingId={order_tracking_id}"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    return response.json()
