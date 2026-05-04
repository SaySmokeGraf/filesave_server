"""Модели для API аут.-авт."""

from pydantic import BaseModel


class Token(BaseModel):
    """Модель токена."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Модель данных из токена."""
    username: str | None = None
    