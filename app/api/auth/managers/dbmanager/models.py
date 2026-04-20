"""Модели для менеджера БД."""

from sqlmodel import Field, SQLModel

from app.api.auth.managers.dbmanager.config import RoleToID


class Role(SQLModel, table=True):
    """Модель-таблица ролей."""
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=20)


class AbscractUser(SQLModel):
    """Абстрактная модель пользователя."""
    username: str
    

class User(AbscractUser, table=True):
    """Модель-таблица пользователей."""
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    hashed_password: str
    role: int = Field(default=RoleToID.UNVERIFIED, foreign_key="role.id")


class UserPublic(AbscractUser):
    """Модель публичных данных о пользователе."""
    id: int
    role: int


class UserCreate(AbscractUser):
    """Модель данных для создания пользователя."""
    hashed_password: str
