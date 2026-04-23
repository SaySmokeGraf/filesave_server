"""Модели для менеджера БД."""

from sqlmodel import Field, SQLModel


class AbscractUser(SQLModel):
    """Абстрактная модель пользователя."""
    username: str
    

class User(AbscractUser, table=True):
    """Модель-таблица пользователей."""
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    hashed_password: str
    is_verified: bool = Field(default=False)
    is_moderator: bool = Field(default=False)
    is_banned: bool = Field(default=False)


class UserPublic(AbscractUser):
    """Модель публичных данных о пользователе."""
    id: int
    is_verified: bool
    is_moderator: bool
    is_banned: bool


class UserCreate(AbscractUser):
    """Модель данных для создания пользователя."""
    hashed_password: str
