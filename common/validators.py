from datetime import date

from rest_framework.exceptions import PermissionDenied


def validate_product_creator_age(birthdate):
    """Проверяет возраст пользователя по birthdate из JWT-токена."""
    if birthdate is None:
        raise PermissionDenied('Укажите дату рождения, чтобы создать продукт.')

    if isinstance(birthdate, str):
        birthdate = date.fromisoformat(birthdate)

    today = date.today()
    age = today.year - birthdate.year - (
        (today.month, today.day) < (birthdate.month, birthdate.day)
    )

    if age < 18:
        raise PermissionDenied('Вам должно быть 18 лет, чтобы создать продукт.')
