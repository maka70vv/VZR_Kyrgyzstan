from django.urls import path

from countries.views import CountryListView, PriceByCountryListView

urlpatterns = [
    path('countries/', CountryListView.as_view(), name='country_list'),
    path('get_insurance_summ/', PriceByCountryListView.as_view(), name='insurance_summ_list')
]
