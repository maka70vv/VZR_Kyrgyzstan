from django.db import models


class Discount(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название (категория) для получения скидки")
    percent = models.IntegerField(verbose_name="Процент скидки (%)", default=0)

    def __str__(self):
        return self.name


class IncreaseFactors(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название повыщающего коэффициента")
    coefficient = models.FloatField(verbose_name="Повышающий коэффициент", default=0)

    def __str__(self):
        return self.name
