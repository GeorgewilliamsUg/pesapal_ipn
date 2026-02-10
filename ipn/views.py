from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def ipn_view(request):
    if request.method == "POST":
        logger.info("IPN received")
        return HttpResponse("IPN received", status=200)
    return HttpResponse("Invalid request", status=400)

def health_check(request):
    return HttpResponse("OK", status=200)
