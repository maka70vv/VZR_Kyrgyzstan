from rest_framework import serializers
from rest_framework.response import Response

from buy_policy.models import BuyPolicy


class BuyPolicySerializer(serializers.ModelSerializer):
    ok = serializers.BooleanField(required=False, default=False)
    message = serializers.CharField(required=False, max_length=255, allow_blank=True, read_only=True)
    _ok_value = None

    class Meta:
        model = BuyPolicy
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        ok = self._ok_value if self._ok_value is not None else data.get('ok', False)
        if not ok:
            data['message'] = 'Невозможно застраховать клиента, так как возраст >= 70 лет или меньше 2 лет'
            return {'message': data['message']}
        return data

    def create(self, validated_data):
        self._ok_value = validated_data.pop('ok', False)
        return super().create(validated_data)


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
