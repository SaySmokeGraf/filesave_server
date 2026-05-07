"""Зависимости для аут.-авт."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from app.api.auth.managers import token_manager, user_manager
from app.api.auth.managers.dbmanager import UserPublic
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


# зависимости в более компактном формате для объявления через аннотирование
GetCurrentUserDep = Annotated[UserPublic, Depends(get_current_user)]


# зависимости по проверке прав доступа
async def get_allowed_user(user: GetCurrentUserDep) -> UserPublic:
    """Получить пользователя, которому разрешено пользоваться сервисом.

    Проверка на наличие верификации от модератора и отсутствие бана.

    Args:
        user (GetCurrentUserDep): Пользователь.

    Raises:
        HTTPException: (403) Пользователь забанен.
        HTTPException: (403) Пользователь не верифицирован модератором.

    Returns:
        UserPublic: Пользователь.
    """
    if user.is_banned:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User is banned by moderator',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    elif not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User is not verified by moderator',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    return user


# зависимости в более компактном формате для объявления через аннотирование
GetAllowedUserDep = Annotated[UserPublic, Depends(get_allowed_user)]


# дополнительные зависимости для получения определенных пар-ров
async def get_user_directory(user: GetAllowedUserDep) -> str:
    """Получить имя папки пользователя.

    Args:
        user (GetAllowedUserDep): Пользователь.

    Returns:
        str: Имя папки пользователя в хранилище.
    """
    return str(user.id)

async def check_user(user: GetAllowedUserDep) -> None:
    """Проверить пользователя.

    Args:
        user (GetAllowedUserDep): Пользователь.
    """
    pass


# зависимости в более компактном формате для объявления через аннотирование
GetUserDirectoryDep = Annotated[str, Depends(get_user_directory)]

# зависимости, возвращающие None, в более компактном формате для использования
# в пар-ре dependencies
CheckUserDepends = Depends(check_user)
