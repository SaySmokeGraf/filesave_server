"""Модели для API аут.-авт."""

from pydantic import BaseModel


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
    