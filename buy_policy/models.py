from django.db import models

from countries.models import Country


class BuyPolicy(models.Model):
    customer_inn = models.CharField(max_length=14, verbose_name="ИНН клиента")
    passport_series_num = models.CharField(max_length=16, verbose_name="Серия и номер паспорта")
    sex = models.CharField(max_length=7, verbose_name="Пол", choices=(("1", "Мужской"), ("2", "Женский")))
    birth_date = models.DateField(verbose_name="Дата рождения")
    email = models.EmailField(verbose_name="Email")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, verbose_name="Отчество", null=True, blank=True)
    phone_number = models.CharField(max_length=25, verbose_name="Номер телефона")
    phone_type = models.CharField(max_length=30, verbose_name="Тип телефона",
                                  choices=(("1", "Домашний"), ("2", "Рабочий"), ("3", "Мобильный")))
    start_date = models.DateField(verbose_name="Дата начала действия полиса")
    end_date = models.DateField(verbose_name="Дата окончания действия полиса")
    territory_and_currency = models.ForeignKey(Country, verbose_name="Территория страхования", on_delete=models.CASCADE)
    purpose = models.CharField(max_length=50, verbose_name="Цель поездки",
                               choices=(("1", "Деловая"), ("2", "Туризм"), ("3", "Гостевая"), ("4", "Спорт"),
                                        ("5", "Воссоединение семьи"), ("6", "Лечение"), ("7", "Стажировка")))
    price_without_taxes_exchange = models.DecimalField(verbose_name="Стоимость без налогов (в иностр. валюте)",
                                                       decimal_places=2, max_digits=4, default=0)
    price_without_taxes_kgs = models.DecimalField(verbose_name="Стоимость без налогов (KGS)", decimal_places=2,
                                                  max_digits=2, default=0)
    taxes_summ = models.DecimalField(verbose_name="Сумма налогов", decimal_places=2, max_digits=2, default=0)
    price_with_taxes_kgs = models.DecimalField(verbose_name="Стоимость с учетом налогов (KGS)", decimal_places=2,
                                               max_digits=2, default=0)
    commission_summ = models.DecimalField(verbose_name="Сумма комиссии", decimal_places=2, max_digits=2, default=0)
    profit_summ = models.DecimalField(verbose_name="Сумма дохода СК", decimal_places=2, max_digits=2, default=0)

    def __str__(self):
        return self.customer_inn