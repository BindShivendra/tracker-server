from datetime import datetime, timedelta, timezone
import pytz
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token


TOKEN_LIFESPAN = settings.TOKEN_LIFESPAN or datetime.timedelta(days=1) 

class ExpiringTokenAuthentication(TokenAuthentication):

    model = Token

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')
        now = datetime.utcnow().replace(tzinfo=pytz.utc)

        if token.created < now - TOKEN_LIFESPAN:
            raise exceptions.AuthenticationFailed('Token has expired')

        return (token.user, token)
