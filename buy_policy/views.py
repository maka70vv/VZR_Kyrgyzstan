from datetime import datetime, date
from decimal import Decimal

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from buy_policy.models import BuyPolicy
from buy_policy.serializers import BuyPolicySerializer, CalculatePolicyPriceSerializer
from buy_policy.services import calculate_insurance_price
from countries.models import PriceByCountry
from exchange_rates.models import DailyExchangeRates


class BuyPolicyView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyPolicySerializer
    queryset = BuyPolicy.objects.all()

    def perform_create(self, serializer):
        travel_agency = self.request.user.travel_agency


class CalculatePriceView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CalculatePolicyPriceSerializer

    def perform_create(self, serializer):
        birth_date = self.request.data.get('birth_date')
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        skiing = bool(self.request.data.get('skiing'))
        sport_activities = bool(self.request.data.get('sport_activities'))
        dangerous_activities = bool(self.request.data.get('dangerous_activities'))
        insurance_summ = self.request.data.get('insurance_summ')
        start_date = datetime.strptime(self.request.data.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(self.request.data.get('end_date'), '%Y-%m-%d').date()
        try:
            insurance_summ = PriceByCountry.objects.get(pk=insurance_summ)
            price = calculate_insurance_price(birth_date, skiing, sport_activities, dangerous_activities, start_date,
                                          end_date, insurance_summ)

            price = Decimal(price)
            if insurance_summ.currency == 'EUR':
                eur_rate = Decimal(
                    DailyExchangeRates.objects.get(date=date.today()).eur_rate)
                price_kgs = round(price * eur_rate, 2)
            elif insurance_summ.currency == 'USD':
                usd_rate = Decimal(
                    DailyExchangeRates.objects.get(date=date.today()).usd_rate)
                price_kgs = round(price * usd_rate, 2)
            elif insurance_summ.currency == 'RUB':
                rub_rate = Decimal(
                    DailyExchangeRates.objects.get(date=date.today()).rub_rate)
                price_kgs = round(price * rub_rate, 2)
            else:
                price_kgs = round(price, 2)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['price'] = price
            serializer.validated_data['price_exchange'] = price_kgs
        except ValueError as e:
            serializer.validated_data['message'] = str(e)
            serializer.is_valid(raise_exception=True)

