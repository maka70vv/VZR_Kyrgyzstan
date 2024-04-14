from django.db import models

from countries.models import Country, PriceByCountry
from discounts.models import AdditionalRisks
from travel_agency.models import TravelAgency
from users.models import User


class BuyPolicy(models.Model):
    policy_id = models.BigIntegerField(primary_key=True, unique=True, editable=False, db_index=True)
    customer_inn = models.CharField(max_length=14, verbose_name="ИНН клиента")
    passport_series_num = models.CharField(max_length=16, verbose_name="Серия и номер паспорта")
    sex = models.CharField(max_length=7, verbose_name="Пол", choices=(("1", "Мужской"), ("2", "Женский")))
    birth_date = models.DateField(verbose_name="Дата рождения")
    email = models.EmailField(verbose_name="Email", null=True, blank=True)
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, verbose_name="Отчество", null=True, blank=True)
    phone_number = models.CharField(max_length=25, verbose_name="Номер телефона", null=True, blank=True)
    phone_type = models.CharField(max_length=30, verbose_name="Тип телефона",
                                  choices=(("1", "Домашний"), ("2", "Рабочий"), ("3", "Мобильный")), null=True,
                                  blank=True, default="3")
    start_date = models.DateField(verbose_name="Дата начала действия полиса")
    end_date = models.DateField(verbose_name="Дата окончания действия полиса")
    territory_and_currency = models.ForeignKey(Country, verbose_name="Территория страхования", on_delete=models.CASCADE)
    insurance_summ = models.ForeignKey(PriceByCountry, verbose_name="Страховая сумма", on_delete=models.CASCADE)
    purpose = models.CharField(max_length=50, verbose_name="Цель поездки",
                               choices=(("1", "Деловая"), ("2", "Туризм"), ("3", "Гостевая"), ("4", "Спорт"),
                                        ("5", "Воссоединение семьи"), ("6", "Лечение"), ("7", "Стажировка")))
    price_exchange = models.DecimalField(verbose_name="Стоимость (в иностр. валюте)",
                                         decimal_places=2, max_digits=10, default=0)
    price_without_taxes_kgs = models.DecimalField(verbose_name="Стоимость без налогов (KGS)", decimal_places=2,
                                                  max_digits=10, default=0)
    taxes_summ = models.DecimalField(verbose_name="Сумма налогов", decimal_places=2, max_digits=10, default=0)
    price_with_taxes_kgs = models.DecimalField(verbose_name="Стоимость с учетом налогов (KGS)", decimal_places=2,
                                               max_digits=10, default=0)
    commission_summ = models.DecimalField(verbose_name="Сумма комиссии", decimal_places=2, max_digits=10, default=0)
    profit_summ = models.DecimalField(verbose_name="Сумма дохода СК", decimal_places=2, max_digits=10, default=0)
    travel_agency = models.ForeignKey(TravelAgency, on_delete=models.SET_NULL, null=True, verbose_name="Тур. агенство")
    travel_agency_worker = models.ForeignKey(User, verbose_name="Сотрудник турагенства", on_delete=models.SET_NULL,
                                             null=True, blank=True)
    risks = models.ManyToManyField(AdditionalRisks, verbose_name="Риски", blank=True)
    is_lapsed = models.BooleanField(verbose_name="Испорчен", default=False)
    sale_date = models.DateField(verbose_name="Дата продажи", null=True, blank=True, auto_now_add=True)
    reported = models.BooleanField(verbose_name="Включен в отчет", default=False)

    def save(self, *args, **kwargs):
        if not self.policy_id:
            last_payment = BuyPolicy.objects.order_by('-policy_id').first()
            if last_payment:
                self.policy_id = last_payment.policy_id + 1
            else:
                self.policy_id = 945  # Initial ID
        super().save(*args, **kwargs)

    def __str__(self):
        return self.customer_inn
