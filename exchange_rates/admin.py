from django.contrib import admin

from exchange_rates.models import DailyExchangeRates


@admin.register(DailyExchangeRates)
class DailyExchangeRatesAdmin(admin.ModelAdmin):
    list_display = ('date', 'usd_rate', 'eur_rate', 'rub_rate')
