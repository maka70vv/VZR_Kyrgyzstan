from datetime import date
from decimal import Decimal

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from buy_policy.serializers import BuyPolicySerializer, CalculatePolicyPriceSerializer
from buy_policy.services import calculate_insurance_price, save_insurance_price
from countries.models import PriceByCountry
from exchange_rates.models import DailyExchangeRates


class BuyPolicyView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyPolicySerializer

    def perform_create(self, serializer):
        travel_agency = self.request.user.travel_agency
        serializer = self.get_serializer(data=self.request.data, many=isinstance(self.request.data, list))
        serializer.is_valid(raise_exception=True)

        for data in serializer.validated_data:  # Итерируемся по каждому словарю в списке данных

            try:

                birth_date = serializer.validated_data.get('birth_date')
                skiing = bool(serializer.validated_data.get('skiing'))
                sport_activities = bool(serializer.validated_data.get('sport_activities'))
                dangerous_activities = bool(serializer.validated_data.get('dangerous_activities'))
                insurance_summ = serializer.validated_data.get('insurance_summ')
                start_date = serializer.validated_data.get('start_date')
                end_date = serializer.validated_data.get('end_date')
                exchange_rates = DailyExchangeRates.objects.get(date=date.today())
                travel_agency_commission = travel_agency.commission
                insured = len(data)

                calculate = save_insurance_price(birth_date, skiing, sport_activities, dangerous_activities,
                                                 start_date, end_date, insurance_summ, exchange_rates, insured,
                                                 travel_agency_commission)

                serializer.validated_data['ok'] = True
                serializer.save(
                    price_exchange=Decimal(calculate['price_exchange']),
                    price_with_taxes_kgs=Decimal(calculate['price_kgs']),
                    taxes_summ=Decimal(calculate['taxes_summ']),
                    price_without_taxes_kgs=Decimal(calculate['price_without_taxes']),
                    commission_summ=Decimal(calculate['commission_summ']),
                    profit_summ=Decimal(calculate['profit']),
                    travel_agency=travel_agency
                )

            except ValueError as e:
                return Response(serializer.validated_data, status=status.HTTP_400_BAD_REQUEST)


class CalculatePriceView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CalculatePolicyPriceSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        response_data = []
        insured = len(self.request.data)

        for data in serializer.validated_data:
            birth_date = data.get('birth_date')
            skiing = bool(data.get('skiing'))
            sport_activities = bool(data.get('sport_activities'))
            dangerous_activities = bool(data.get('dangerous_activities'))
            insurance_summ = data.get('insurance_summ')
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            try:
                exchange_rates = DailyExchangeRates.objects.get(date=date.today())
                insurance_summ = PriceByCountry.objects.get(pk=insurance_summ)
                price = calculate_insurance_price(birth_date, skiing, sport_activities, dangerous_activities,
                                                  start_date,
                                                  end_date, insurance_summ, exchange_rates, insured)

                response_data.append(price)
            except ValueError as e:
                response_data.append({'message': str(e)})
        return Response(response_data, status=status.HTTP_200_OK)
