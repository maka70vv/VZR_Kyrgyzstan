from django.contrib import admin

from buy_policy.models import BuyPolicy


@admin.register(BuyPolicy)
class BuyPolicyAdmin(admin.ModelAdmin):
    list_display = ('customer_inn', 'last_name', 'first_name', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
