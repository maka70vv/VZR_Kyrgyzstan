from django.db import models


class TravelAgency(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название турагенства")
    inn = models.CharField(max_length=14, verbose_name="ИНН компании", unique=True)
    commission = models.IntegerField(verbose_name="Комиссионное вознаграждение (%)", default=0)

    def __str__(self):
        return self.name
