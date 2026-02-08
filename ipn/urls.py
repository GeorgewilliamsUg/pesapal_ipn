from django.urls import path
from .views import pesapal_ipn

urlpatterns = [
    path('pesapal_ipn/', pesapal_ipn, name='pesapal_ipn'),

]