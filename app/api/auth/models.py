"""Модели для API аутентификации-авторизации"""

from pydantic import BaseModel


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
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Модель данных из токена.
    
    Params:
        username (str | None): Имя пользователя. По умолчанию None.
    """
    username: str | None = None
    