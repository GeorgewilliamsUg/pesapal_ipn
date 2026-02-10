from django.core.management.base import BaseCommand
from django.conf import settings
import requests


class Command(BaseCommand):
    help = "Register Pesapal IPN URL and print notification_id"

    def handle(self, *args, **options):
        self.stdout.write("Registering Pesapal IPN URL...")

        token = self.get_access_token()
        ipn_id = self.register_ipn(token)

        self.stdout.write(
            self.style.SUCCESS(
                f"IPN registered successfully. notification_id = {ipn_id}"
            )
        )

    def get_access_token(self):
        url = f"{settings.PESAPAL_BASE_URL}/api/Auth/RequestToken"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        payload = {
            "consumer_key": settings.PESAPAL_CONSUMER_KEY,
            "consumer_secret": settings.PESAPAL_CONSUMER_SECRET,
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=15,
        )

        try:
            data = response.json()
        except ValueError:
            raise RuntimeError(
                f"Pesapal auth returned non-JSON response: {response.text}"
            )

        if response.status_code != 200:
            raise RuntimeError(
                f"Pesapal auth failed ({response.status_code}): {data}"
            )

        token = data.get("token")
        if not token:
            raise RuntimeError(
                f"Pesapal auth response missing token: {data}"
            )

        return token


    def register_ipn(self, token):
        url = f"{settings.PESAPAL_BASE_URL}/api/URLSetup/RegisterIPN"

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        payload = {
            "url": "https://pesapal-ipn-n3h3.onrender.com/ipn/",
            "ipn_notification_type": "POST",
        }

        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()

        data = response.json()
        return data["ipn_id"]
