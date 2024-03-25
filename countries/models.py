from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название страны")

    def __str__(self):
        return self.name


class PriceByCountry(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Страна")
    currency = models.CharField(verbose_name="Валюта для покупки полиса", max_length=3, choices=(
        ('EUR', 'EUR'),
        ('USD', 'USD'),
        ('KGZ', 'KGZ'),
        ('RUB', 'RUB')
    ))
    insurance_summ = models.IntegerField(verbose_name="Страховая сумма")
    price_up_to_7days = models.IntegerField(verbose_name="Стоимость 1-7 дней")
    price_up_to_15days = models.IntegerField(verbose_name="Стоимость 8-15 дней")
    price_up_to_30days = models.IntegerField(verbose_name="Стоимость 16-30 дней")
    price_up_to_90days = models.IntegerField(verbose_name="Стоимость 31-90 дней")
    price_up_to_180days = models.IntegerField(verbose_name="Стоимость 91-180 дней")
    price_up_to_365days = models.IntegerField(verbose_name="Стоимость 181-365 дней")

    def __str__(self):
        return self.country.name
