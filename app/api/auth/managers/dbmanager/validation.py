"""Валидация для менеджера БД."""

from fastapi import HTTPException, status

from app.api.utils.validation import isvalid_username_filter


# получение валидных полей моделей
def get_valid_username_filter(username: str | None) -> str | None:
    """Получить валидный фильтр по имени поьзователя.

    Args:
        username (str | None): Имя пользователя.

    Raises:
        HTTPException: (422) Невалидный фильтр по имени пользователя.

    Returns:
        str | None: Имя пользователя.
    """
    if not isvalid_username_filter(username):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='Bad username filter'
        )
    return username
