from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from base.models import Ride


class RideSerializer(ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'bus_company', 'average_speed', 'cities', 'is_express',
                  'price', 'cities_where_collect_passengers']

        extra_kwargs = {'cities_where_collect_passengers': {'required': True, 'write_only': True}}


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'required': True, 'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class RideMiniSerializer(ModelSerializer):
    class Meta:
        model = Ride
        fields = ['bus_company', 'cities', 'is_express', 'price']