"""Роутер под API аутентификации-авторизации."""

from fastapi import APIRouter, HTTPException, status

from app.api.auth.dependencies import (
    GetCurrentUserDep, GetValidRegData, GetValidLoginData
)
from app.api.auth.managers import token_manager, user_manager, UserPublic
from app.api.auth.models import Token


router = APIRouter()


@router.post('/token')
async def login_for_access_token(form_data: GetValidLoginData) -> Token:
    """Вход пользователя.

    Args:
        form_data (OAuth2FormDep): Данные формы для аутентификации по паролю.

    Raises:
        HTTPException: (401) Неправильный логин или пароль.

    Returns:
        Token: Токен для данного пользователя типа bearer.
    """
    user = user_manager.authenticate_user(form_data.username,
                                          form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token = token_manager.create_token(data={'sub': user.username})
    return Token(access_token=access_token, token_type='bearer')

@router.post('/register')
async def register_for_access_token(reg_data: GetValidRegData) -> Token:
    """Регистрация пользователя.

    Args:
        reg_data (GetRegFormDataDep): Данные формы для аутентификации по
            паролю.
    
    Raises:
        HTTPException: (403) Пользователь с таким логином уже существует.

    Returns:
        Token: Токен для данного пользователя типа bearer.
    """
    user = user_manager.create_user(reg_data.username, reg_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User already exists',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token = token_manager.create_token(data={'sub': user.username})
    return Token(access_token=access_token, token_type='bearer')

@router.get('/user-info', response_model=UserPublic)
async def get_user_info(user: GetCurrentUserDep) -> UserPublic:
    """Получить информацию о пользователе.

    Args:
        user (GetCurrentUserDep): Пользователь.

    Returns:
        UserPublic: Публичная информация о пользователе.
    """
    return user
