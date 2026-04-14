"""Роутер под API авторизации-аутентификации."""

from fastapi import APIRouter, HTTPException, status

from app.api.auth.dependencies import OAuth2FormDep
from app.api.auth.managers import token_manager, user_manager
from app.api.auth.models import Token


router = APIRouter()


@router.post('/token')
async def login_for_access_token(form_data: OAuth2FormDep) -> Token:
    user = user_manager.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token = token_manager.create_token(data={'sub': user.username})
    return Token(access_token=access_token, token_type='bearer')

@router.post('/register')
async def register_for_access_token(form_data: OAuth2FormDep) -> Token:
    user_manager.save_user(form_data.username, form_data.password)
    access_token = token_manager.create_token(data={'sub': form_data.username})
    return Token(access_token=access_token, token_type='bearer')
