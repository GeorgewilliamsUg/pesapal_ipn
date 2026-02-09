from django.http import HttpResponse
import logging
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@csrf_exempt
def pesapal_ipn(request):
    data = request.GET.dict() or request.POST.dict()
    logger.info("Received IPN data", extra={"data": data})

    return HttpResponse("IPN received", status=200)
