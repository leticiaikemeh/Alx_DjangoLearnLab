# accounts/views.py
from rest_framework import generics, permissions, response, status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, LoginSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        super_response = super().create(request, *args, **kwargs)
        user = self.get_serializer().instance
        token = Token.objects.get(user=user)
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "token": token.key, 
        }
        return response.Response(data, status=status.HTTP_201_CREATED)


class LoginView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.save()
        return response.Response(data, status=status.HTTP_200_OK)


