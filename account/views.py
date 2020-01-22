from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import generics, permissions

from .models import CustomUser
from .serializers import UserSerializer, UserRegisterSerializer, UserUpdateSerializer, UserPasswordSerializer , GetTokenSerializer


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


class GetAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = GetTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = CustomUser.objects.get(email=email)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


get_token = GetAuthToken.as_view()