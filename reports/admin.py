from django.contrib import admin

from reports.models import Report, Invoice


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('travel_agency', 'date')
    list_filter = ('date', 'travel_agency')


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('travel_agency', 'date')
    list_filter = ('date', 'travel_agency')
