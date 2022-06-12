from django.urls import path
from .views import *

urlpatterns = [
    path('', get_routes),
    path('rides/', get_rides),
    path('rides/<str:pk>/', get_ride),
]