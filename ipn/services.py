import requests
from django.conf import settings


def get_access_token():
    url = "https://pay.pesapal.com/v3/api/Auth/RequestToken"

    payload = {
        "consumer_key": settings.PESAPAL_CONSUMER_KEY,
        "consumer_secret": settings.PESAPAL_CONSUMER_SECRET,
    }

    response = requests.post(url, json=payload, timeout=15)
    response.raise_for_status()

    data = response.json()

    if "token" not in data:
        raise Exception(f"Invalid token response from Pesapal: {data}")

    return data["token"]


def verify_payment(order_tracking_id):
    token = get_access_token()

    url = (
        "https://pay.pesapal.com/v3/api/Transactions/GetTransactionStatus"
        f"?orderTrackingId={order_tracking_id}"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    return response.json()
