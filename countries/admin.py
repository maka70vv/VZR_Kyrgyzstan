from django.contrib import admin

from countries.models import Country, PriceByCountry


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(PriceByCountry)
class PriceByCountryAdmin(admin.ModelAdmin):
    search_fields = ('country__name',)
    list_display = ('country', 'insurance_summ')
    list_filter = ('insurance_summ', 'currency')
