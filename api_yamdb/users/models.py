"""Обновленная модель пользователя."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    """Модель пользователя с дополнительнвым полем."""
    is_moderator = models.BooleanField('Модератор', default=False)
