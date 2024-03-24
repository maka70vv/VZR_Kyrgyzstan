from django.urls import include, path
from rest_framework import routers

from .views import UsersViewSet, UserRegistrationAPIView

router = routers.DefaultRouter()
router.register(r"users", UsersViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserRegistrationAPIView.as_view(), name="register")
]

