from django.shortcuts import render
from .models import Ride


def get_rides_plan(request):
    plan = Ride.objects.all()

    context = {'plan': plan}

    return render(request, 'all-connections.html', context)