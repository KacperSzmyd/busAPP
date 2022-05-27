from django.contrib import admin

from base.models import Ride

# admin.site.register(Ride)

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ['bus_company', 'is_express']
