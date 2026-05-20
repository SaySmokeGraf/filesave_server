"""Роутер API модерирования."""

from fastapi import APIRouter, Depends

from app.api.auth.dependencies import CheckModeratorDepends
from app.api.auth.managers import user_manager
from app.api.auth.managers import (
    PagedUsersPublic, PaginationParams, UsersFilterParams
)


router = APIRouter()


@router.get('/users/', dependencies=[CheckModeratorDepends],
            response_model=PagedUsersPublic)
async def get_users(pagination: PaginationParams = Depends(),
                    filters: UsersFilterParams = Depends()) -> PagedUsersPublic:
    """Получить страницу из списка пользователей.

    Args:
        pagination (PaginationParams): Параметры пагинации.
        filters (UsersFilterParams): Параметры фильтрации.

    Returns:
        PagedUsersPublic: Страница из списка пользователей.
    """
    return user_manager.get_users(pagination, filters)
