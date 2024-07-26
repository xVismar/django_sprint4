from datetime import date

from django.core.exceptions import ValidationError


def check_pub_date(value: date) -> None:
    age = (date.today() - value).days / 365
    if age < 1 or age > 120:
        raise ValidationError(
            'Ожидается возраст от 1 года до 120 лет'
        )

