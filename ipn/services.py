import requests
from django.conf import settings
import uuid


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

    payload = {
        "id": str(uuid.uuid4()),
        "currency": data["currency"],
        "amount": float(data["amount"]),
        "description": "Nissi Medical Outreach Donation",
        "callback_url": "https://nissi-website.github.io/thank-you.html",
        "notification_id": settings.PESAPAL_IPN_ID,
        "billing_address": {
            "email_address": data["email"],
            "first_name": data["first_name"],
            "last_name": data["last_name"],
            "country_code": "UG",
        },
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers, timeout=15)
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
