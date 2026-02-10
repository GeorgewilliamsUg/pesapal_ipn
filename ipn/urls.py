from django.urls import path
from django.http import JsonResponse
from django.urls import path
from .views import ipn_view
from .api import create_order

def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path("", health_check),
    path("ipn/", ipn_view),
    path("create-order/", create_order),
]

