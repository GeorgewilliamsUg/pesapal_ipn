import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import verify_payment


@csrf_exempt
def ipn_view(request):
    order_tracking_id = request.GET.get("OrderTrackingId")
    notification_type = request.GET.get("OrderNotificationType")

    if not order_tracking_id or not notification_type:
        return JsonResponse({"status": 400})

    try:
        payment = verify_payment(order_tracking_id)
    except Exception:
        return JsonResponse({"status": 500})

    return JsonResponse({
        "orderNotificationType": notification_type,
        "orderTrackingId": order_tracking_id,
        "status": 200,
    })


# Backwards-compatible name used by urls.py
@csrf_exempt
def pesapal_ipn(request):
    return ipn_view(request)
