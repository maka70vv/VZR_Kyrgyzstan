from django.urls import path

from buy_policy.views import CalculatePriceView, BuyPolicyView, PoliciesByTravelAgencyView, DestroyPolicyView

urlpatterns = [
    path('calculate_price/', CalculatePriceView.as_view(), name='calculate_price'),
    path("save_policy/", BuyPolicyView.as_view(), name="save_policy"),
    path("get_policies/", PoliciesByTravelAgencyView.as_view(), name="get_policies"),
    path("destroy_policy/<int:pk>/", DestroyPolicyView.as_view(), name="destroy_policy")
]
