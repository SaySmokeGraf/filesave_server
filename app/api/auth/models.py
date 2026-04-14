"""Модели для API аут.-авт."""

from pydantic import BaseModel


class Token(BaseModel):
    """Модель токена."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Модель данных из токена."""
    username: str | None = None


class User(BaseModel):
    """Общая модель пользователя."""
    username: str


class UserInDB(User):
    """Модель пользователя как элемента БД."""
    hashed_password: str
    