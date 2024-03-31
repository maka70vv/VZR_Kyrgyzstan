from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from countries.models import Country, PriceByCountry
from countries.serializers import CountrySerializer, PriceByCountrySerializer


class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]


class PriceByCountryListView(generics.ListAPIView):
    serializer_class = PriceByCountrySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        country = self.request.query_params.get('country')
        try:
            insurance_summ = PriceByCountry.objects.filter(country=country)
            return Response({'insurance_summ': insurance_summ}, status=status.HTTP_200_OK)
        except PriceByCountry.DoesNotExist:
            return Response({'message': 'Выбрана неверная страна. Повторите ввод'}, status=status)
