from django.db import models

from travel_agency.models import TravelAgency


class Report(models.Model):
    travel_agency = models.ForeignKey(TravelAgency, on_delete=models.SET_NULL, null=True, verbose_name="Турагенство")
    file = models.FileField(upload_to='reports/', verbose_name="Отчет")
    date = models.DateField(verbose_name="Дата формирования", auto_now_add=True)

    def __str__(self):
        return self.travel_agency.name
