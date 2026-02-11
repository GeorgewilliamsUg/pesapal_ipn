import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .services import submit_order


@csrf_exempt
def create_order(request):
    if request.method == "OPTIONS":
        return HttpResponse(status=204)

    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    required = ["amount", "currency", "first_name", "last_name", "email"]
    if any(k not in data or not data[k] for k in required):
        return JsonResponse({"error": "Missing required fields"}, status=400)

    try:
        pesapal_response = submit_order(data)
    except Exception:
        return JsonResponse({"error": "Payment initiation failed"}, status=502)

    checkout_url = pesapal_response.get("redirect_url")
    if not checkout_url:
        return JsonResponse({"error": "No checkout URL"}, status=502)

    return JsonResponse({"checkout_url": checkout_url})
