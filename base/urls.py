from django.urls import path
from .views import *

urlpatterns = [
    path('', get_rides_plan, name="plan")
]