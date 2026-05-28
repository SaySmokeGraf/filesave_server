"""Зависимости для API модерации."""

from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.api.auth.managers import user_manager
from app.api.utils.validation import isvalid_username


# зависимости и их компактные записи для объявления через аннотирование
async def get_valid_username(username: str) -> str:
    """Получить валидное имя пользователя.

    Args:
        username (str): Имя пользователя.

    Raises:
        HTTPException: (422) Невалидное имя пользователя.

    Returns:
        str: Имя пользователя без изменений.
    """
    if not isvalid_username(username):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='Invalid username'
        )
    return username


GetValidUsername = Annotated[str, Depends(get_valid_username)]


async def get_allowed_username(username: GetValidUsername) -> str:
    """Получить имя пользователя, над которым можно производить модерацию.

    Args:
        username (GetValidUsername): Имя пользователя.

    Raises:
        HTTPException: (404) Пользователь не найден.
        HTTPException: (403) Недостаточно прав для модерирования пользователя.

    Returns:
        str: Имя пользователя без изменений.
    """
    user = user_manager.get_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    if user.is_moderator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='No permission to delete or update another moderator'
        )
    return username


GetAllowedUsernameDep = Annotated[str, Depends(get_allowed_username)]
