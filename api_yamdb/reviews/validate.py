from django.core.exceptions import ValidationError
from django.utils import timezone

from .constants import MAX_SCORE_VALUE, MIN_SCORE_VALUE


def validate_year(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError('Указанный Вами год еще не наступил')


def validate_score(value):
    if not (MIN_SCORE_VALUE <= value <= MAX_SCORE_VALUE):
        raise ValidationError('Проверьте оценку!')
    return value
