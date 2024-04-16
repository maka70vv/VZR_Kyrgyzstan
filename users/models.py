from django.contrib.auth.models import AbstractUser
from django.db import models

from travel_agency.models import TravelAgency


class User(AbstractUser):
    inn = models.CharField(max_length=14, verbose_name="ИНН", null=True, blank=True)
    travel_agency = models.ForeignKey(TravelAgency, on_delete=models.CASCADE, verbose_name="Туркомпания", null=True, blank=True)
    is_travel_agency_staff = models.BooleanField(default=False, verbose_name="Администратор туркомпании")

    def __str__(self):
        return self.inn
