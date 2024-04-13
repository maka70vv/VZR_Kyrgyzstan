from datetime import date
from decimal import Decimal

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from mail_users.mail import send_notification_on_save, send_notification_to_user_on_save
from buy_policy.models import BuyPolicy
from buy_policy.serializers import BuyPolicySerializer, CalculatePolicyPriceSerializer
from buy_policy.services import calculate_insurance_price, save_insurance_price
from countries.models import PriceByCountry
from exchange_rates.models import DailyExchangeRates
from mail_users.models import MailUser


class BuyPolicyView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyPolicySerializer
    queryset = BuyPolicy.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        if not isinstance(data, list):
            return Response({"message": "Request body must be a list of dictionaries"},
                            status=status.HTTP_400_BAD_REQUEST)

        responses = []
        email_users = MailUser.objects.all()
        for item in data:
            serializer = self.get_serializer(data=item)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']
            birth_date = serializer.validated_data.get('birth_date')
            risks = serializer.validated_data.get('risks')
            insurance_summ = serializer.validated_data.get('insurance_summ')
            start_date = serializer.validated_data.get('start_date')
            end_date = serializer.validated_data.get('end_date')
            exchange_rates = DailyExchangeRates.objects.get(date=date.today())
            travel_agency = self.request.user.travel_agency
            travel_agency_commission = travel_agency.commission
            territory_and_currency = serializer.validated_data.get('territory_and_currency')
            insured = len(data)

            try:
                calculate = save_insurance_price(birth_date, risks,
                                                 start_date, end_date, insurance_summ, exchange_rates, insured,
                                                 travel_agency_commission)
                id = 1

                serializer.save(
                    policy_id=id,
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
                send_notification_on_save(travel_agency.name, email_users)
                send_notification_to_user_on_save(email, calculate['price_kgs'])
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
            risks = data.get('risks')
            insurance_summ = data.get('insurance_summ')
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            try:
                exchange_rates = DailyExchangeRates.objects.get(date=date.today())
                insurance_summ = PriceByCountry.objects.get(pk=insurance_summ)
                price = calculate_insurance_price(birth_date, risks,
                                                  start_date,
                                                  end_date, insurance_summ, exchange_rates, insured)

                response_data.append(price)
            except ValueError as e:
                response_data.append({'message': str(e)})
        return Response(response_data, status=status.HTTP_200_OK)


class PoliciesByTravelAgencyView(generics.ListAPIView):
    serializer_class = BuyPolicySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        travel_agency = self.request.user.travel_agency
        return BuyPolicy.objects.filter(travel_agency=travel_agency)


class DestroyPolicyView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyPolicySerializer
    queryset = BuyPolicy.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        travel_agency = self.request.user.travel_agency
        if (instance.sale_date - date.today()).days <= 3 and instance.travel_agency == travel_agency:
            instance.is_lapsed = True
            instance.save()
            return Response({'message': 'Полис помечен как испорченный'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Невозможно удалить полис. С момента продажи прошло более 3 дней'},
                            status=status.HTTP_400_BAD_REQUEST)
