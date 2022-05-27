from django.shortcuts import render, redirect
from .models import Ride


def check_bus_route(bus, start, stop):
    cities_in_route = bus.cities_where_collect_passengers
    if start in cities_in_route and stop in cities_in_route:
        if cities_in_route.index(start) < cities_in_route.index(stop):
            return True
    return False


def get_rides_plan(request):
    plan = Ride.objects.all()

    context = {'plan': plan}

    return render(request, 'all-connections.html', context)


def find_bus(request):
    method = 'GET'
    if request.method == 'POST':
        method = 'POST'
        first_point = request.POST.get('first_stop').title()
        last_point = request.POST.get('end_stop').title()
        express = request.POST.get('express')

        # taking plan for all express busses
        express_busses = Ride.objects.filter(is_express=True)
        # checking if any bus cover first and last point and if it is going in right direction
        filtered_express_busses = [bus for bus in express_busses if check_bus_route(bus, first_point, last_point)]

        # taking plan for all non-express busses
        standard_busses = Ride.objects.filter(is_express=False)
        # checking if any non-express bus cover first and last point and if it is going in right direction
        standard_busses = [bus for bus in standard_busses if check_bus_route(bus, first_point, last_point)]

        context = {'express_busses': filtered_express_busses,
                   'standard_busses': standard_busses,
                   'is_express': express,
                   'method': method}
        return render(request, 'home.html', context)

    context = {'method': method}
    return render(request, 'home.html', context)


def get_single_bus(request, pk):
    bus = Ride.objects.get(id=pk)
    cities = bus.cities_where_collect_passengers.split(',')
    context = {'bus': bus,
               'cities': cities}
    return render(request, 'bus.html', context)
