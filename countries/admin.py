from django.contrib import admin

from countries.models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'currency')
    search_fields = ('name')
