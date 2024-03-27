from datetime import date
from decimal import Decimal

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from buy_policy.models import BuyPolicy
from buy_policy.serializers import BuyPolicySerializer, CalculatePolicyPriceSerializer
from buy_policy.services import calculate_insurance_price, save_insurance_price
from countries.models import PriceByCountry, Country
from exchange_rates.models import DailyExchangeRates


class BuyPolicyView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyPolicySerializer
    queryset = BuyPolicy.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        if not isinstance(data, list):
            return Response({"detail": "Request body must be a list of dictionaries"},
                            status=status.HTTP_400_BAD_REQUEST)

        responses = []
        for item in data:
            serializer = self.get_serializer(data=item)
            serializer.is_valid(raise_exception=True)
            birth_date = serializer.validated_data.get('birth_date')
            skiing = bool(serializer.validated_data.get('skiing'))
            sport_activities = bool(serializer.validated_data.get('sport_activities'))
            dangerous_activities = bool(serializer.validated_data.get('dangerous_activities'))
            insurance_summ = serializer.validated_data.get('insurance_summ')
            start_date = serializer.validated_data.get('start_date')
            end_date = serializer.validated_data.get('end_date')
            exchange_rates = DailyExchangeRates.objects.get(date=date.today())
            travel_agency = self.request.user.travel_agency
            travel_agency_commission = travel_agency.commission
            territory_and_currency = serializer.validated_data.get('territory_and_currency')
            insured = len(data)

            try:
                calculate = save_insurance_price(birth_date, skiing, sport_activities, dangerous_activities,
                                                 start_date, end_date, insurance_summ, exchange_rates, insured,
                                                 travel_agency_commission)

                serializer.save(
                    price_exchange=Decimal(calculate['price_exchange']),
                    price_with_taxes_kgs=Decimal(calculate['price_kgs']),
                    taxes_summ=Decimal(calculate['taxes_summ']),
                    price_without_taxes_kgs=Decimal(calculate['price_without_taxes']),
                    commission_summ=Decimal(calculate['commission_summ']),
                    profit_summ=Decimal(calculate['profit']),
                    travel_agency=travel_agency,
                    territory_and_currency=territory_and_currency,
                    insurance_summ=insurance_summ,
                )
                responses.append(serializer.data)
            except ValueError as e:
                responses.append({"message": str(e)})

        return Response(responses, status=status.HTTP_200_OK)


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
