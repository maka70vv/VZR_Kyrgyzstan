from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response

from travel_agency.models import TravelAgency
from .models import User
from .serializers import UserSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        inn = request.data.get("inn")
        try:
            TravelAgency.objects.get(inn=inn)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except TravelAgency.DoesNotExist:
            return Response({"message": "Туристическое агенство не зарегистрированно в системе"},
                            status=status.HTTP_400_BAD_REQUEST)
