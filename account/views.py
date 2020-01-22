from rest_framework import generics, permissions

from .models import CustomUser
from .serializers import UserSerializer, UserRegisterSerializer, UserUpdateSerializer, UserPasswordSerializer


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'slug'


class UserRegisterView(generics.CreateAPIView):
    model = CustomUser

    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserRegisterSerializer


class UserUpdateView(generics.UpdateAPIView):
    model = CustomUser
    lookup_field = 'slug'
    queryset = CustomUser.objects.all()
    permission_classes = [
        permissions.AllowAny 
    ]
    serializer_class = UserUpdateSerializer

class PasswordUpdateView(generics.UpdateAPIView):
    model = CustomUser
    lookup_field = 'slug'
    queryset = CustomUser.objects.all()
    permission_classes = [
        permissions.AllowAny 
    ]
    serializer_class = UserPasswordSerializer

