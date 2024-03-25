from rest_framework import serializers

from travel_agency.models import TravelAgency
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        try:
            agency = TravelAgency.objects.get(inn=validated_data.get("inn"))
            user.travel_agency = agency
            user.is_travel_agency = True
            user.save()
        except TravelAgency.DoesNotExist:
            pass
        return user
