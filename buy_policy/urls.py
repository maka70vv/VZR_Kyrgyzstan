from django.urls import path

from buy_policy.views import CalculatePriceView

urlpatterns = [
    path('calculate_price/', CalculatePriceView.as_view(), name='calculate_price')
]
