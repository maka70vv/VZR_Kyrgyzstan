from django.contrib import admin

from travel_agency.models import TravelAgency


@admin.register(TravelAgency)
class TravelAgencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'inn', 'commission')
    search_fields = ('name', 'inn')
