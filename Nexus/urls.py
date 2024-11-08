from django.urls import path
from .views import *

urlpatterns = [
    path('broker/<slug:broker_code>/place-order/', BrokerPlaceOrder.as_view(), name='place_order'),
]