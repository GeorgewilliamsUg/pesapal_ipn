from django.urls import path
from django.http import JsonResponse
from .views import ipn_view
from .api import create_order

def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path("", ipn_view, name="pesapal_ipn"),
    path("health/", health_check, name="health"),
    path("create-order/", create_order, name="create_order"),
]
