"""Customized validators."""

from django.core.exceptions import ValidationError


def do_not_use_me(value):
    if value.lower() == 'me':
        raise ValidationError('Do not use "me" as a username!')
