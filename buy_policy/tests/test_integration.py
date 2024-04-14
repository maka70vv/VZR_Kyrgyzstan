from datetime import date

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from buy_policy.integration import send_policy
from buy_policy.models import BuyPolicy
from countries.models import PriceByCountry, Country
from discounts.models import AdditionalRisks
from exchange_rates.models import DailyExchangeRates
from travel_agency.models import TravelAgency
from users.models import User


class BuyPolicyAPITests(APITestCase):
    def test_create_buy_policy(self):
        agency = TravelAgency.objects.create(name="Test Agency", inn='12345678', commission=10)
        user = User.objects.create_user(username='testuser', password='testpassword', inn="12345678",
                                             travel_agency=agency)
        exchange_rates = DailyExchangeRates.objects.create(eur_rate=1.2, usd_rate=1.0, rub_rate=0.014, date=date.today())
        country = Country.objects.create(name="Test Country")
        insurance_summ = PriceByCountry.objects.create(country=country, currency='USD',
                                      insurance_summ=1000, price_up_to_7days=100, price_up_to_15days=200,
                                      price_up_to_30days=300, price_up_to_90days=400, price_up_to_180days=500,
                                      price_up_to_365days=600)
        risks = AdditionalRisks.objects.create(name="Test Risk", percent=2, crm_id=1)
        policy = BuyPolicy.objects.create(
            customer_inn="373298287",
            passport_series_num="string",
            sex="1",
            birth_date="1993-11-07",
            email="skkgstan@gmail.com",
            last_name="string",
            first_name="string",
            patronymic="string",
            phone_number="string",
            phone_type="1",
            start_date="2024-09-24",
            end_date="2024-09-25",
            purpose="1",
            territory_and_currency=country,
            insurance_summ=insurance_summ,
            price_exchange=10,
            price_without_taxes_kgs=100,
            price_with_taxes_kgs=130,
            commission_summ=10,
            profit_summ=90,
        )

        policy.risks.set([risks])

        data = send_policy(policy)
        self.assertEqual(data['customer_individual']['passport']['inn'], '373298287')
        self.assertEqual(data['customer_individual']['passport']['series_number'], 'string')
        self.assertEqual(data['customer_individual']['passport']['sex'], '1')
        self.assertEqual(data['customer_individual']['passport']['birth_date'], "1993-11-07")
        self.assertEqual(data['customer_individual']['last_name'], 'string')
        self.assertEqual(data['customer_individual']['first_name'], 'string')
        self.assertEqual(data['customer_individual']['patronymic'], 'string')
        self.assertEqual(data['policy_number'], 'ВЗР-945')
        self.assertEqual(data['start_date'], "2024-09-24")
        self.assertEqual(data['end_date'], "2024-09-25")
        self.assertEqual(data['purpose'], '1')
        self.assertEqual(data['currency_letter_code'], "USD")
        self.assertEqual(data['sum_insured'], 1000)
        self.assertEqual(data['insurance_premium'], 130)
        self.assertEqual(data['territory'], 'Test Country')
        self.assertEqual(data['additional_info'], [1])
