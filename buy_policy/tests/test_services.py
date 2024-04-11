from datetime import date
from django.test import TestCase

from discounts.models import AdditionalRisks
from exchange_rates.models import DailyExchangeRates
from countries.models import PriceByCountry, Country
from buy_policy.services import (
    calculate_age,
    calculate_coefficient,
    calculate_price,
    convert_to_kgs,
    calculate_taxes,
    calculate_price_with_taxes,
    calculate_commission_summ,
    calculate_profit,
    save_insurance_price,
    calculate_insurance_price
)


class TestUtilsFunctions(TestCase):
    def setUp(self):
        self.birth_date = date(1990, 1, 1)
        self.start_date = date(2024, 4, 1)
        self.end_date = date(2024, 4, 10)
        self.insurance_summ = PriceByCountry(country=Country.objects.create(name="Test Country"), currency='USD',
                                             insurance_summ=1000, price_up_to_7days=100, price_up_to_15days=200,
                                             price_up_to_30days=300, price_up_to_90days=400, price_up_to_180days=500,
                                             price_up_to_365days=600)
        self.exchange_rates = DailyExchangeRates(eur_rate=1.2, usd_rate=1.0, rub_rate=0.014)
        self.insured = 1
        self.commission = 10

    def test_calculate_age(self):
        age = calculate_age(self.birth_date)
        self.assertEqual(age, 34)  # Проверяем, что возраст вычисляется корректно

    def test_calculate_coefficient(self):
        risks = AdditionalRisks.objects.create(name="Test Risk", percent=2, crm_id=1)
        coefficient = calculate_coefficient(30, risks,
                                            insured=5)
        self.assertEqual(coefficient, 2)  # Проверяем, что коэффициент вычисляется корректно

    def test_calculate_price(self):
        price = calculate_price(5, 2, self.insurance_summ)
        self.assertEqual(price, 1000)  # Проверяем, что цена вычисляется корректно

    def test_convert_to_kgs(self):
        price_kgs = convert_to_kgs(100, self.insurance_summ, self.exchange_rates)
        self.assertEqual(price_kgs, 100)  # Проверяем, что конвертация в KGS работает корректно

    def test_calculate_taxes(self):
        taxes = calculate_taxes(100)
        self.assertEqual(taxes, 30)  # Проверяем, что налоги вычисляются корректно

    def test_calculate_price_with_taxes(self):
        price_with_taxes = calculate_price_with_taxes(100, 30)
        self.assertEqual(price_with_taxes, 130)  # Проверяем, что цена с налогами вычисляется корректно

    def test_calculate_commission_summ(self):
        commission_summ = calculate_commission_summ(100, self.commission)
        self.assertEqual(commission_summ, 10)  # Проверяем, что комиссия вычисляется корректно

    def test_calculate_profit(self):
        profit = calculate_profit(100, 10)
        self.assertEqual(profit, 90)  # Проверяем, что прибыль вычисляется корректно

    def test_save_insurance_price(self):
        risks = AdditionalRisks.objects.create(name="Test Risk", percent=4, crm_id=1)
        prices = save_insurance_price(self.birth_date, risks,
                                      start_date=self.start_date, end_date=self.end_date,
                                      insurance_summ=self.insurance_summ,
                                      exchange_rates=self.exchange_rates, insured=self.insured,
                                      commission=self.commission)
        self.assertEqual(prices['age'], 34)  # Проверяем, что возраст сохраняется корректно
        self.assertEqual(prices['price_kgs'], 9360)  # Проверяем, что цена в KGS сохраняется корректно
        self.assertEqual(prices['price_exchange'], 9360)  # Проверяем, что цена в валюте сохраняется корректно

    def test_calculate_insurance_price(self):
        risks = AdditionalRisks.objects.create(name="Test Risk", percent=4, crm_id=1)
        prices = calculate_insurance_price(self.birth_date, risks,
                                           start_date=self.start_date, end_date=self.end_date,
                                           insurance_summ=self.insurance_summ,
                                           exchange_rates=self.exchange_rates, insured=self.insured)
        self.assertEqual(prices['price_kgs'], 9360)  # Проверяем, что цена в KGS вычисляется корректно
        self.assertEqual(prices['price_exchange'], 9360)  # Проверяем, что цена в валюте вычисляется корректно
