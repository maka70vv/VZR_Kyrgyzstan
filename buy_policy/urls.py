from django.urls import path

from buy_policy.views import CalculatePriceView, BuyPolicyView

urlpatterns = [
    path('calculate_price/', CalculatePriceView.as_view(), name='calculate_price'),
    path("save_policy/", BuyPolicyView.as_view(), name="save_policy")
]
