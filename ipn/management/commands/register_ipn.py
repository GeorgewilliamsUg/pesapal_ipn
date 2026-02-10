from django.core.management.base import BaseCommand
from django.conf import settings
import requests
from ipn.services import get_access_token


class Command(BaseCommand):
    help = "Register Pesapal IPN URL and print notification_id"

    def handle(self, *args, **options):
        self.stdout.write("Registering Pesapal IPN URL...")
        token = get_access_token()
        ipn_id = self.register_ipn(token)

        self.stdout.write(
            self.style.SUCCESS(
                f"IPN registered successfully. notification_id = {ipn_id}"
            )
        )


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
