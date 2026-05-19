"""Роутер API модерирования."""

from fastapi import APIRouter

from app.api.auth.dependencies import CheckModeratorDepends
from app.api.auth.managers import user_manager, UserPublic


router = APIRouter()


@router.get('/users/get', dependencies=[CheckModeratorDepends])
async def get_users() -> list[UserPublic]:
    """Получить список пользователей.

    Returns:
        list[UserPublic]: Список пользователей.
    """
    return user_manager.get_users()
