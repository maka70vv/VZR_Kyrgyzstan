from django.contrib import admin

from discounts.models import Discount, AdditionalRisks


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'percent')
    search_field = 'name'


@admin.register(AdditionalRisks)
class AdditionalRisksAdmin(admin.ModelAdmin):
    list_display = ('name', 'percent', 'crm_id')
    search_field = 'name'
