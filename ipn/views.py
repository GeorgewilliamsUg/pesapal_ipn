from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from .services import verify_payment

logger = logging.getLogger(__name__)

@csrf_exempt
def ipn_view(request):
    if request.method != "POST":
        return HttpResponse("Invalid request", status=400)

    try:
        payload = json.loads(request.body.decode())
        order_tracking_id = payload.get("OrderTrackingId")
        merchant_reference = payload.get("MerchantReference")

        logger.info("IPN received: %s", payload)

        if not order_tracking_id:
            return HttpResponse("Missing tracking id", status=400)

        status = verify_payment(order_tracking_id)
        logger.info("Pesapal verification: %s", status)

        if status.get("payment_status_description") == "COMPLETED":
            logger.info("Payment completed for %s", merchant_reference)

        return HttpResponse("IPN received", status=200)

    except Exception as e:
        logger.exception("IPN processing failed")
        return HttpResponse("IPN error", status=200)

def health_check(request):
    return HttpResponse("OK", status=200)
