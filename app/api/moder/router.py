"""Роутер API модерирования.

Contains:
    router: Роутер API модерирования.
"""

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import JSONResponse

import app.api.moder._swagger_docs as swdocs
from app.api.auth.dependencies import CheckModeratorDepends
from app.api.auth.managers import (
    user_manager,
    PagedUsersPublic, PaginationParams, UsersFilterParams, UserUpdateRights
)
from app.api.files.utils.file_utils import delete_user_directory
from app.api.moder.dependencies import AllowedUsernameDep


router = APIRouter(
    dependencies=[CheckModeratorDepends], **swdocs.router.docs_dump()
)


@router.get('/users', response_model=PagedUsersPublic,
            **swdocs.endpoints.get_users.docs_dump())
async def get_users(
    pagination: PaginationParams = Depends(),
    filters: UsersFilterParams = Depends()
) -> PagedUsersPublic:
    """Получить страницу из списка пользователей.

    Args:
        pagination (PaginationParams): Параметры пагинации. Модель
            разворачивается в отдельные query-параметры.
        filters (UsersFilterParams): Параметры фильтрации. Модель
            разворачивается в отдельные query-параметры.

    Returns:
        PagedUsersPublic: Страница из списка пользователей.
    """
    return user_manager.get_users(pagination, filters)

@router.delete('/users/delete', **swdocs.endpoints.delete_user.docs_dump())
async def delete_user(username: AllowedUsernameDep) -> JSONResponse:
    """Удалить пользователя.

    Args:
        username (AllowedUsernameDep): Имя пользователя. Зависимость.

    Raises:
        HTTPException: (409) Нет доступа для удаления (например, сервис в
            данный момент занял папку пользователя для какой-либо обработки).

    Returns:
        JSONResponse: Ответ об успешном выполнении.
    """
    user = user_manager.get_user(username)
    try:
        delete_user_directory(user.dir_name)
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='No permissions to delete'
        )
    
    deleted_user = user_manager.delete_user(username)  
    return JSONResponse(
        content={'message': f'User {deleted_user.username} deleted successfully!'}
    )

@router.patch('/users/update', **swdocs.endpoints.update_user.docs_dump())
async def update_user_rights(
    username: AllowedUsernameDep,
    user_rights: UserUpdateRights = Body(
        **swdocs.params.update_rights.docs_dump()
    )
) -> JSONResponse:
    """Обновить права доступа пользователя.

    Args:
        username (AllowedUsernameDep): Имя пользователя. Зависимость.
        user_rights (UserUpdateRights): Обновления прав пользователя.

    Returns:
        JSONResponse: Ответ об успешном выполнении.
    """
    updated_user = user_manager.update_user_rights(username, user_rights)
    return JSONResponse(
        content={'message': f'User {updated_user.username} updated successfully!'}
    )
