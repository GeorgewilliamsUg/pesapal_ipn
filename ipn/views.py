from django.http import HttpResponse
import logging


logger = logging.getLogger(__name__)


def pesapal_ipn(request):
    data = request.GET.dict() or request.POST.dict()
    logger.info(f"Received IPN data", extra={"data": data})

  
    return HttpResponse("IPN received", status=200)
    

