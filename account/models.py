from django.db import models
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .utils import unique_slug_generator, random_string_generator



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class UserManger(BaseUserManager):
    """ 
    Make emailas unique identifiers for authentication instead of usernames.
    """
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    slug = models.SlugField(unique=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManger()

    @property
    def username(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)



pre_save.connect(pre_save_receiver, sender=CustomUser)