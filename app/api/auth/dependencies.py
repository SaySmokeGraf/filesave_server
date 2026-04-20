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


async def get_current_user(token: OAuth2SchemeDep) -> UserPublic:
    """Получить текущего пользователя по токену.

    Args:
        token (OAuth2SchemeDep): Токен.

    Raises:
        HTTPException: Невалидные данные для входа.

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
