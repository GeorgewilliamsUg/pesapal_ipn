import json
import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@csrf_exempt
def ipn_view(request):
    if request.method != "POST":
        return HttpResponse("Method not allowed", status=405)

    try:
        payload = request.body.decode("utf-8")
        logger.info("Pesapal IPN received: %s", payload)

        # STEP 1: Parse incoming data
        data = json.loads(payload)

        order_tracking_id = data.get("OrderTrackingId")
        merchant_reference = data.get("MerchantReference")
        status = data.get("Status")

        if not order_tracking_id:
            logger.warning("Missing OrderTrackingId")
            return HttpResponse("Invalid payload", status=400)

        # STEP 2: VERIFY payment server-to-server
        # This MUST call Pesapal's verification API
        # Do NOT trust the IPN blindly

        # verification_result = verify_payment(order_tracking_id)

        # STEP 3: Persist result (DB or log)
        logger.info(
            "Payment update | ref=%s | tracking=%s | status=%s",
            merchant_reference,
            order_tracking_id,
            status
        )

        # STEP 4: Respond fast
        return HttpResponse("OK", status=200)

    except Exception as e:
        logger.exception("IPN processing failed")
        return HttpResponse("Server error", status=500)
