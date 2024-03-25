from rest_framework import serializers

from buy_policy.models import BuyPolicy


class BuyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyPolicy
        fields = '__all__'
