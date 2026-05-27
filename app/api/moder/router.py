"""Роутер API модерирования."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.api.auth.dependencies import CheckModeratorDepends
from app.api.auth.managers import user_manager
from app.api.auth.managers import (
    PagedUsersPublic, PaginationParams, UsersFilterParams
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
        HTTPException: (403) Попытка модератора удалить другого модератора.
        HTTPException: (409) Нет доступа для удаления (например, сервис в
            занял папку пользователя для обработки в данный момент).
        HTTPException: (404) Пользователь с таким именем не найден.

    Returns:
        JSONResponse: Ответ об успешном выполнении.
    """
    user = user_manager.get_user(username)
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
    if deleted_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            details='User not found'
        )
    
    return JSONResponse(
        content={'message': f'User {deleted_user.username} deleted successfully!'}
    )
