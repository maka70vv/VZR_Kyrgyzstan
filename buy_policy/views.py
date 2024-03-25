from datetime import datetime

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from buy_policy.models import BuyPolicy
from buy_policy.serializers import BuyPolicySerializer
from buy_policy.services import calculate_insurance_price


class BuyPolicyView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyPolicySerializer
    queryset = BuyPolicy.objects.all()

    def perform_create(self, serializer):
        travel_agency = self.request.user.travel_agency


class CalculatePriceView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuyPolicySerializer

    def perform_create(self, serializer):
        birth_date = self.request.data.get('birth_date')
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        skiing = bool(self.request.data.get('skiing'))
        sport_activities = bool(self.request.data.get('sport_activities'))
        dangerous_activities = bool(self.request.data.get('dangerous_activities'))
        insurance_summ = self.request.data.get('insurance_summ')
        start_date = datetime.strptime(self.request.data.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(self.request.data.get('end_date'), '%Y-%m-%d').date()

        price = calculate_insurance_price(birth_date, skiing, sport_activities, dangerous_activities, start_date,
                                          end_date, insurance_summ)
        return Response({'price': price}, status=status.HTTP_200_OK)

