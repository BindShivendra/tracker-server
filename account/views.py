from datetime import datetime, timedelta, timezone
import pytz
from django.conf import settings
from django.views.generic.edit import FormView
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import generics, permissions

from .models import CustomUser
from .serializers import UserSerializer, UserRegisterSerializer, UserUpdateSerializer, UserPasswordSerializer , GetTokenSerializer
from account import  forms

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
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            token.created = datetime.utcnow()
            token.save()
        token_lifespan = settings.TOKEN_LIFESPAN
        now = datetime.utcnow()

        if token.created < now - token_lifespan:
            token.delete()
            token = Token.objects.create(user=user)
            token.create = now
            token.save()

        return Response({'token': token.key})


get_token = GetAuthToken.as_view()

class SignUpView(FormView):
    template_name = 'account/signup.html'
    form_class = forms.UserCreationForm

    def get_success_url(self):
        redirect_to  = self.request.GET.get('next', '/')
        return redirect_to

    def form_valid(self, form):
        res = super().form_valid(form)
        form.save()
        
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')

        logger.info(f'New sign up for {email} view SignUpView')

        user = authenticate(email=email, password=password)
        login(self.request, user)

        form.send_email()
        messages.info(self.request, 'You signed up successfully.')

        return res

signup = SignUpView.as_view()