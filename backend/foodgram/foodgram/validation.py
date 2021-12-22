from django.core.exceptions import ValidationError


def validate_under_zero(value):
    if value <= 0:
        raise ValidationError('Параметр не может быть меньше или равен 0')
