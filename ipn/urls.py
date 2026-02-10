from django.urls import path
from . import views, api

app_name = "ipn"

urlpatterns = [
    path("", views.pesapal_ipn, name="pesapal_ipn"),
    path("create-order/", api.create_order, name="create_order"),
]