from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    now = timezone.now().year
    if value > now:
        raise ValidationError('Указанный Вами год еще не наступил')


def validate_score(self, value):
    if not (1 <= value <= 10):
        raise ValidationError('Проверьте оценку!')
    return value
