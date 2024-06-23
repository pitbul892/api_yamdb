from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# https://docs.djangoproject.com/en/3.2/ref/models/fields/#enumeration-types

class MyUser(AbstractUser):
    """
    Кастомизированная модель пользователя.
    """

    class Role(models.TextChoices):
        USER = 'user', _('user')
        MODERATOR = 'moderator', _('moderator')
        ADMIN = 'admin', _('admin')

    role = models.CharField(
        max_length=9,
        choices=Role.choices,
        default=Role.USER,
    )
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    bio = models.TextField('biography', blank=True)
    confirmation_code = models.CharField(
        max_length=256,
        blank=True,
    )

    def is_admin(self):
        return self.role == 'admin'

    def is_moderator(self):
        return self.role == 'moderator'
