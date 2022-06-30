from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .serializers import RideSerializer, UserSerializer, RideMiniSerializer
from base.models import Ride


class RideSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    pagination_class = RideSetPagination
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        ride = self.get_object()
        ride.bus_company = request.data.get('bus_company', ride.bus_company)
        ride.average_speed = request.data.get('average_speed', ride.average_speed)
        ride.cities_where_collect_passengers = request.data.get('cities_where_collect_passengers',
                                                                ride.cities_where_collect_passengers)
        ride.is_express = request.data.get('is_express', ride.is_express)
        ride.price = request.data.get('price', ride.price)
        ride.save()
        serializer = RideSerializer(ride, many=False)
        return Response(serializer.data)

    # Ride objects which contains city taken from query param in 'bus.cities_where_collect_passengers'
    @action(detail=False, methods=['get'])
    def routes(self, request, *args, **kwargs):
        q = self.request.query_params['city']
        rides = Ride.objects.all()
        list_of_ids = [bus.id for bus in rides if q in bus.cities_where_collect_passengers]
        output = Ride.objects.filter(pk__in=list_of_ids)

        serializer = RideMiniSerializer(output, many=True)
        return Response(serializer.data)
