from django.db import models


class Ride(models.Model):
    bus_company = models.CharField(max_length=100, blank=False, null=False)
    average_speed = models.PositiveSmallIntegerField(default=75)
    cities_where_collect_passengers = models.TextField(blank=False, null=False)
    is_express = models.BooleanField(default=False)
    price = models.PositiveSmallIntegerField(default=25)

    def __str__(self):
        stations_list = self.cities_where_collect_passengers.split(",")
        return '{} {} - {}'.format(self.bus_company, stations_list[0], stations_list[-1])