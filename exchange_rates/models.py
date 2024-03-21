from django.db import models


class DailyExchangeRates(models.Model):
    usd_rate = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Курс USD")
    eur_rate = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Курс EUR")
    rub_rate = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Курс RUB")
    date = models.DateField(verbose_name="Дата курса")

    def __str__(self):
        return str(self.date)
