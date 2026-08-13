"""Зависимости для аутентификации-авторизации.

Dependencies:
    oauth2_scheme: OAuth2 схема.
    get_valid_reg_data: Валидные данные регистрации.
    get_valid_login_data: Валидные данные входа.
    get_current_user: Текущий пользователь.
    get_allowed_user: Пользователь с правами доступа использования сервиса.
    get_moderator: Модератор.
    get_user_directory: Имя папки пользователя.

AnnotatedDeps:
    OAuth2SchemeDep (str): OAuth2 схема.
    OAuth2FormDep (OAuth2PasswordRequestForm): Форма OAuth2 для аутентификации.
    RegDataDep (AuthFormData): Валидные данные регистрации.
    LoginDataDep (AuthFormData): Валидные данные входа.
    CurrentUserDep (UserPublic): Текущий пользователь.
    AllowedUserDep (UserPublic): Пользователь с правами доступа использования
        сервиса.
    ModerDep (UserPublic): Модератор.
    UserDirDep (str): Имя папки пользователя.

CheckDepends:
    CheckUserDepends: Проверка пользователя.
    CheckModeratorDepends: Проверка модератора.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from app.api.auth.managers import token_manager, user_manager
from app.api.auth.managers.dbmanager import UserPublic
from app.api.auth.models import AuthFormData, TokenData
from app.api.utils.validation import (
    isvalid_pwd, isvalid_pwd_length, isvalid_username, isvalid_username_length
)


# базовые зависимости для OAuth2 аутентификации по паролю bearer типа
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')
OAuth2SchemeDep = Annotated[str, Depends(oauth2_scheme)]
OAuth2FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


# зависимости валидации данных формы
async def get_valid_reg_data(form_data: OAuth2FormDep) -> AuthFormData:
    """Получить валидные данные формы для регистрации.

    Args:
        form_data (OAuth2FormDep): Данные формы.
    
    Raises:
        HTTPException: (422) Невалидное поле формы.

    Returns:
        AuthFormData: Данные для регистрации.
    """
    is_valid = isvalid_pwd(form_data.password)
    is_valid = is_valid and isvalid_username(form_data.username)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='Could not validate registration credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    return AuthFormData(
        username=form_data.username,
        password=form_data.password
    )

async def get_valid_login_data(form_data: OAuth2FormDep) -> AuthFormData:
    """Получить валидные данные формы для входа.

    Args:
        form_data (OAuth2FormDep): Данные формы.

    Raises:
        HTTPException: (401) Невалидное поле формы.

    Returns:
        AuthFormData: Данные для входа.
    """
    is_valid = isvalid_pwd_length(form_data.password)
    is_valid = is_valid and isvalid_username_length(form_data.username)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    return AuthFormData(
        username=form_data.username,
        password=form_data.password
    )


# зависимости в более компактном формате для объявления через аннотирование
RegDataDep = Annotated[AuthFormData, Depends(get_valid_reg_data)]
LoginDataDep = Annotated[AuthFormData, Depends(get_valid_login_data)]


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
CurrentUserDep = Annotated[UserPublic, Depends(get_current_user)]


# зависимости по проверке прав доступа с их компактными вариантами
async def get_allowed_user(user: CurrentUserDep) -> UserPublic:
    """Получить пользователя, которому разрешено пользоваться сервисом.

    Проверка на наличие верификации от модератора и отсутствие бана.

    Args:
        user (CurrentUserDep): Пользователь.

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


AllowedUserDep = Annotated[UserPublic, Depends(get_allowed_user)]


async def get_moderator(user: AllowedUserDep) -> UserPublic:
    """Получить пользователя с правами модератора.

    Args:
        user (AllowedUserDep): Пользователь.

    Raises:
        HTTPException: (403) Пользователь не является модератором.

    Returns:
        UserPublic: Пользователь.
    """
    if not user.is_moderator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User is not a moderator',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    return user


ModerDep = Annotated[UserPublic, Depends(get_moderator)]


# зависимости в формате для использования в параметре dependencies без
# дальнейшего использования возвращаемых значений
CheckUserDepends = Depends(get_allowed_user)
CheckModeratorDepends = Depends(get_moderator)


# дополнительные зависимости для получения определенных параметров
async def get_user_directory(user: AllowedUserDep) -> str:
    """Получить имя папки пользователя.

    Args:
        user (AllowedUserDep): Пользователь.

    Returns:
        str: Имя папки пользователя в хранилище.
    """
    return user.dir_name


# зависимости в более компактном формате для объявления через аннотирование
UserDirDep = Annotated[str, Depends(get_user_directory)]
