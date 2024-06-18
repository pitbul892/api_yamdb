from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    is_moderator = models.BooleanField('Модератор', default=False)
