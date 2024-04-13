from datetime import date

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from countries.models import PriceByCountry, Country
from discounts.models import AdditionalRisks
from exchange_rates.models import DailyExchangeRates
from travel_agency.models import TravelAgency
from users.models import User


class BuyPolicyAPITests(APITestCase):
    def setUp(self):
        agency = TravelAgency.objects.create(name="Test Agency", inn='12345678', commission=10)
        self.user = User.objects.create_user(username='testuser', password='testpassword', inn="12345678", travel_agency=agency)
        self.token = self.get_token(self.user)
        DailyExchangeRates.objects.create(eur_rate=1.2, usd_rate=1.0, rub_rate=0.014, date=date.today())
        PriceByCountry.objects.create(country=Country.objects.create(name="Test Country"), currency='USD',
                                      insurance_summ=1000, price_up_to_7days=100, price_up_to_15days=200,
                                      price_up_to_30days=300, price_up_to_90days=400, price_up_to_180days=500,
                                      price_up_to_365days=600)

    def get_token(self, user):
        access = AccessToken.for_user(user)
        return str(access)

    def test_create_buy_policy(self):
        AdditionalRisks.objects.create(name="Test Risk", percent=2, crm_id=1)
        data = [{
            "customer_inn": "373298287",
            "passport_series_num": "string",
            "sex": "1",
            "birth_date": "1993-11-07",
            "email": "skkgstan@gmail.com",
            "last_name": "string",
            "first_name": "string",
            "patronymic": "string",
            "phone_number": "string",
            "phone_type": "1",
            "start_date": "2024-09-24",
            "end_date": "2024-09-25",
            "purpose": "1",
            "risks": [1],
            "territory_and_currency": 1,
            "insurance_summ": 1
        }]
        url = reverse('save_policy')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.post(url, data, format='json')

        self.assertEqual(float(response.data[0]['price_with_taxes_kgs']), 260)
        self.assertEqual(float(response.data[0]['price_without_taxes_kgs']), 200)
        self.assertEqual(float(response.data[0]['commission_summ']), 20)
        self.assertEqual(float(response.data[0]['profit_summ']), 180)
        self.assertEqual(float(response.data[0]['price_exchange']), 260)
        self.assertEqual(float(response.data[0]['taxes_summ']), 60)
