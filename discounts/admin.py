from django.contrib import admin

from discounts.models import Discount


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'percent')
    search_field = 'name'
