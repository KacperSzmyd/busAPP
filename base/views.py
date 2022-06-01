from django.shortcuts import render
from .models import Ride


def check_bus_route(bus, start, stop):
    cities_in_route = bus.cities_where_collect_passengers
    if str(start) in cities_in_route and str(stop) in cities_in_route:
        if cities_in_route.index(start) < cities_in_route.index(stop):
            return True
    return False


def all_to_city(bus, end):
    cities_in_route = bus.cities_where_collect_passengers.split(',')
    if str(end) in cities_in_route and cities_in_route.index(end) != 0:
        return True
    return False


def all_from_city(bus, start):
    cities_in_route = bus.cities_where_collect_passengers.split(',')
    if start in cities_in_route and cities_in_route.index(start) != len(cities_in_route)-1:
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
        first_point = request.POST.get('first_stop').strip().title()
        last_point = request.POST.get('end_stop').strip().title()
        express = request.POST.get('express')

        # taking plan for all express busses
        express_busses = Ride.objects.filter(is_express=True)

        # taking plan for all non-express busses
        standard_busses = Ride.objects.filter(is_express=False)

        # covering empty first point case
        if first_point == '':
            filtered_express_busses = [bus for bus in express_busses if all_to_city(bus, last_point)]
            filtered_standard_busses = [bus for bus in standard_busses if all_to_city(bus, last_point)]
            context = {'express_busses': filtered_express_busses,
                       'standard_busses': filtered_standard_busses,
                       'is_express': express,
                       'method': method}
            return render(request, 'home.html', context)

        # covering empty last point case
        if last_point is None or last_point == '':
            filtered_express_busses = [bus for bus in express_busses if all_from_city(bus, first_point)]
            filtered_standard_busses = [bus for bus in standard_busses if all_from_city(bus, first_point)]
            context = {'express_busses': filtered_express_busses,
                       'standard_busses': filtered_standard_busses,
                       'is_express': express,
                       'method': method}
            return render(request, 'home.html', context)

        # checking if any bus cover first and last point and if it is going in right direction
        filtered_express_busses = [bus for bus in express_busses if check_bus_route(bus, first_point, last_point)]

        # checking if any non-express bus cover first and last point and if it is going in right direction
        filtered_standard_busses = [bus for bus in standard_busses if check_bus_route(bus, first_point, last_point)]

        context = {'express_busses': filtered_express_busses,
                   'standard_busses': filtered_standard_busses,
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
