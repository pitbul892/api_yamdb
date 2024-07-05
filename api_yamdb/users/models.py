from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import (
    ADMIN,
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_USERNAME,
    MAX_LENGTH_ROLE,
    MODERATOR,
    USER,
)
from .validators import do_not_use_me


class ModifiedUser(AbstractUser):
    """
    Кастомизированная модель пользователя.
    """

    class Role(models.TextChoices):
        USER = USER
        MODERATOR = MODERATOR
        ADMIN = ADMIN

    role = models.CharField(
        max_length=MAX_LENGTH_ROLE,
        choices=Role.choices,
        default=Role.USER,
    )
    email = models.EmailField(
        _('email address'),
        max_length=MAX_LENGTH_EMAIL,
        unique=True
    )
    bio = models.TextField('biography', blank=True)
    username = models.CharField(
        _('username'),
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
        help_text=_('Letters, digits and @/./+/-/_ only.'),
        validators=[
            UnicodeUsernameValidator(),
            do_not_use_me
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    @property
    def is_admin(self):
        return (
            self.role == ADMIN or self.is_superuser or self.is_staff
        )

    @property
    def is_moderator(self):
        return self.role == MODERATOR
