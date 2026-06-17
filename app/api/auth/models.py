"""Модели для API аутентификации-авторизации.

Models:
    AuthFormData: Данные формы аутентификации по паролю.
    Token: Модель токена.
    TokenData: Модель данных из токена.
"""

from pydantic import BaseModel, Field

import app.api.auth._swagger_docs as swdocs


class AuthFormData(BaseModel):
    """Данные формы аутентификации по паролю.
    
    Params:
        username (str): Имя пользователя.
        password (str): Пароль.
    """
    username: str
    password: str


class Token(BaseModel):
    """Модель токена.
    
    Params:
        access_token (str): Токен.
        token_type (str): Тип токена.
    """
    model_config = swdocs.models.token.docs_dump()

    access_token: str = Field(**swdocs.fields.access_token.docs_dump())
    token_type: str = Field(**swdocs.fields.token_type.docs_dump())


class TokenData(BaseModel):
    """Модель данных из токена.
    
    Params:
        username (str | None): Имя пользователя. По умолчанию None.
    """
    username: str | None = None
    