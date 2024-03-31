from buy_policy import serializers
from countries.models import Country, PriceByCountry
from rest_framework import serializers


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class PriceByCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceByCountry
        fields = '__all__'
