import logging
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.forms import UsernameField
from django.core.mail import send_mail

from account import models

logger = logging.getLogger(__name__)

class UserCreationForm(DjangoUserCreationForm):

    class Meta(DjangoUserCreationForm.Meta):
        model = models.CustomUser
        fields = ('email',)
        field_class = {'email': UsernameField}

    def send_email(self):
        logger.info(f'Sending sign up email from {self.cleaned_data["email"]}')
        msg = f'Wecome  {self.cleaned_data["email"]}.'
        send_mail(
            'Welcome to BookShop',
            msg,
            'site@bookshop.domain',
            [self.cleaned_data["email"]],
            fail_silently=False,
        )

class AuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(strip=False, widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user = authenticate(self.request, email=email, password=password)
            if self.user is None:
                raise forms.ValidationError(
                        "Email or Password is incorrect"
                        )
            logger.info(f'Authentication for {email} successful')
        return self.cleaned_data

    def get_user(self):
        return self.user