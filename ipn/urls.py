from django.http import JsonResponse
from django.urls import path
from .views import ipn_view

def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path("", health_check),
    path("ipn/", ipn_view),
]
