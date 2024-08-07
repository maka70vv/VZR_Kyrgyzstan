from rest_framework import serializers
from rest_framework.response import Response

from buy_policy.models import BuyPolicy


class BuyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyPolicy
        fields = '__all__'
        extra_kwargs = {'reported': {'write_only': True}}


class CalculatePolicyPriceSerializer(serializers.Serializer):
    birth_date = serializers.DateField()
    skiing = serializers.BooleanField(default=False)
    sport_activities = serializers.BooleanField(default=False)
    dangerous_activities = serializers.BooleanField(default=False)
    insurance_summ = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    price = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True, required=False)
    price_exchange = serializers.DecimalField(max_digits=12, decimal_places=2, allow_null=True, required=False)
    message = serializers.CharField(max_length=500, required=False)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data.get('price') is not None and data.get('price_exchange') is not None:
            return {
                'price': data['price'],
                'price_exchange': data['price_exchange']
            }
        elif 'message' in data:
            return {
                "message": data['message']
            }
        return data
