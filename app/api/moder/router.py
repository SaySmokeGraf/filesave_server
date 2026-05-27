"""Роутер API модерирования."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.api.auth.dependencies import CheckModeratorDepends
from app.api.auth.managers import user_manager
from app.api.auth.managers import (
    PagedUsersPublic, PaginationParams, UsersFilterParams, UserUpdateRights
)
from app.api.files.utils.file_utils import delete_user_directory


router = APIRouter(dependencies=[CheckModeratorDepends])


@router.get('/users', response_model=PagedUsersPublic)
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

@router.delete('/users/delete')
async def delete_user(username: str) -> JSONResponse:
    """Удалить пользователя.

    Args:
        username (str): Имя пользователя.

    Raises:
        HTTPException: (404) Пользователь с таким именем не найден.
        HTTPException: (403) Попытка модератора удалить другого модератора.
        HTTPException: (409) Нет доступа для удаления (например, сервис в
            занял папку пользователя для обработки в данный момент).

    Returns:
        JSONResponse: Ответ об успешном выполнении.
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
            detail='Moderator has no permission to delete another moderator'
        )
    
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

@router.patch('/users/update')
async def update_user_rights(username: str,
                             user_rights: UserUpdateRights) -> JSONResponse:
    """Обновить права доступа пользователя.

    Args:
        username (str): Имя пользователя.
        user_rights (UserUpdateRights): Обновления прав пользователя.

    Raises:
        HTTPException: (404) Пользователь с таким именем не найден.
        HTTPException: (403) Попытка модератора изменить другого модератора.

    Returns:
        JSONResponse: Ответ об успешном выполнении.
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
            detail='Moderator has no permission to update another moderator'
        )
    
    updated_user = user_manager.update_user_rights(username, user_rights)
    return JSONResponse(
        content={'message': f'User {updated_user.username} updated successfully!'}
    )
