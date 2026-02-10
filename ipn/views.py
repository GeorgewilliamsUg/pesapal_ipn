from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def ipn_view(request):
    return JsonResponse({
        "status": "ok",
        "method": request.method,
    })

@csrf_exempt
def create_order(request):
    return JsonResponse({
        "method": request.method,
        "body_raw": str(request.body),
        "content_type": request.content_type,
    })
