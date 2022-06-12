from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RideSerializer
from base.models import Ride


@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api',
        'GET /rides',
        'GET /rides/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def get_rides(request):
    rides = Ride.objects.all()
    rides_serializer = RideSerializer(rides, many=True)
    return Response(rides_serializer.data)


@api_view(['GET'])
def get_ride(request, pk):
    ride = Ride.objects.get(id=pk)
    ride_serializer = RideSerializer(ride, many=False)
    return Response(ride_serializer.data)

