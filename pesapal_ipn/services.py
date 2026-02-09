import requests
from django.conf import settings


def get_access_token():
    url = f"{settings.PESAPAL_BASE_URL}/api/Auth/RequestToken"

    response = requests.post(
        url,
        json={
            "consumer_key": settings.PESAPAL_CONSUMER_KEY,
            "consumer_secret": settings.PESAPAL_CONSUMER_SECRET,
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()["token"]


def verify_payment(order_tracking_id):
    token = get_access_token()

    url = (
        f"{settings.PESAPAL_BASE_URL}"
        f"/api/Transactions/GetTransactionStatus"
        f"?orderTrackingId={order_tracking_id}"
    )

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    return response.json()
