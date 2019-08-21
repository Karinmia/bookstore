import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from .utils import generate_token, get_file_path


def get_time_hence(days=2):
    return timezone.now + timezone.timedelta(days=days)


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True, help_text="email as username")
    photo = models.FileField(upload_to=get_file_path, default=settings.USER_DEFAULT_AVATAR_PATH, help_text="profile photo")
    affiliate_code = models.CharField(max_length=45, unique=False, default=generate_token)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.email



class Affiliate(models.Model):
    date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, related_name='owned_affiliates', on_delete=models.CASCADE)
    member = models.ForeignKey(User, related_name='participating_affiliates', null=True, blank=True, on_delete=models.SET_NULL)


class PasswordReset(models.Model):
    user = models.ForeignKey(User, related_name='requested_reset', on_delete=models.CASCADE)
    reset_key = models.CharField(max_length=45, unique=False, default=generate_token)
    expired = models.BooleanField(default=False)
