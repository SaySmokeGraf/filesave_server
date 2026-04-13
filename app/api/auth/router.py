"""Роутер под API авторизации-аутентификации."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from app.api.auth.managers import token_manager, user_manager
from app.api.auth.models import Token, TokenData


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
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


@router.post('/token')
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
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
async def register_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user_manager.save_user(form_data.username, form_data.password)
    access_token = token_manager.create_token(data={'sub': form_data.username})
    return Token(access_token=access_token, token_type='bearer')
