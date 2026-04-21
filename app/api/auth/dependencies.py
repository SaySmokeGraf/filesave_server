"""Зависимости для аут.-авт."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from app.api.auth.managers import token_manager, user_manager
from app.api.auth.managers.dbmanager import RoleToID, UserPublic
from app.api.auth.models import TokenData


# базовые зависимости для OAuth2 аутентификации по паролю bearer типа
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')
OAuth2SchemeDep = Annotated[str, Depends(oauth2_scheme)]
OAuth2FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


# основная универсальная зависимость
async def get_current_user(token: OAuth2SchemeDep) -> UserPublic:
    """Получить текущего пользователя по токену.

    Args:
        token (OAuth2SchemeDep): Токен.

    Raises:
        HTTPException: (401) Невалидные данные для входа.

    Returns:
        UserPublic: Данные о пользователе.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = token_manager.decode_token(token)
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = user_manager.get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


# зависимость в более компактном формате для объявления через аннотирование
GetCurrentUserDep = Annotated[UserPublic, Depends(get_current_user)]


# дополнительные зависимости с параметрами доступа по роли
async def get_user_directory(user: GetCurrentUserDep) -> str:
    """Получить имя папки пользователя.

    Args:
        user (GetCurrentUserDep): Пользователь.

    Raises:
        HTTPException: (403) Нет доступа из-за неподходящей роли пользователя.

    Returns:
        str: Имя папки пользователя в хранилище.
    """
    if user.role == RoleToID.USER or user.role == RoleToID.ADMIN:
        return str(user.id)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Access denied due to user role permissions',
            headers={'WWW-Authenticate': 'Bearer'}
        )


# зависимость в более компактном формате для объявления через аннотирование
GetUserDirectoryDep = Annotated[str, Depends(get_user_directory)]
