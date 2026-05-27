"""Модели для менеджера БД."""

from __future__ import annotations
from typing import Any

from fastapi import Query
from pydantic import BaseModel, field_validator
from sqlmodel import col, Field, SQLModel

from app.api.auth.managers.dbmanager.validation import (
    get_valid_username_filter,
)


# модели пользователя
class AbscractUser(SQLModel):
    """Абстрактная модель пользователя.
    
    Params:
        username (str): Имя пользователя.
    """
    username: str
    

class User(AbscractUser, table=True):
    """Модель-таблица пользователей.
    
    Params:
        id (int | None): ID пользователя. PRIMARY KEY. По умолчанию None.
            Предполагается использование сугубо стандартного значения для того,
            чтобы ID пользователя назначала БД.
        username (str): Имя пользователя. UNIQUE.
        hashed_password (str): Хешированный пароль.
        is_verified (bool): Флаг верифицированности пользователя. По умолчанию
            False.
        is_moderator (bool): Флаг, является ли пользователь модератором. По
            умолчанию False.
        is_banned (bool): Флаг забаненности пользователя. По умолчанию False.
    """
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    hashed_password: str
    is_verified: bool = Field(default=False)
    is_moderator: bool = Field(default=False)
    is_banned: bool = Field(default=False)


class UserPublic(AbscractUser):
    """Модель публичных данных о пользователе.
    
    Params:
        id (int): ID пользователя.
        username (str): Имя пользователя.
        is_verified (bool): Флаг верифицированности пользователя.
        is_moderator (bool): Флаг, является ли пользователь модератором.
        is_banned (bool): Флаг забаненности пользователя.
        dir_name (str): Имя папки в хранилище.
    """
    id: int
    is_verified: bool
    is_moderator: bool
    is_banned: bool
    
    @property
    def dir_name(self) -> str:
        """Имя папки пользователя."""
        return str(self.id)


class UserCreate(AbscractUser):
    """Модель данных для создания пользователя.
    
    Params:
        username (str): Имя пользователя.
        hashed_password (str): Хешированный пароль.
    """
    hashed_password: str


# вспомогательные модели
class AbstractPagedItems(BaseModel):
    """Абстрактная страница из списка объектов.
    
    Params:
        items (list[Any]): Список объектов на странице.
        total (int): Общее число объектов.
        page (int): Номер страницы.
        limit (int): Максимальное количество объектов на странице.
    """
    items: list[Any]
    total: int
    page: int
    limit: int


class PagedUsers(AbstractPagedItems):
    """Cтраница из списка пользователей.
    
    Params:
        items (list[User]): Список пользователей на странице.
        total (int): Общее число пользователей.
        page (int): Номер страницы.
        limit (int): Максимальное количество пользователей на странице.
    """
    items: list[User]


class PagedUsersPublic(AbstractPagedItems):
    """Страница из списка публичных моделей пользователей.
    
    Params:
        items (list[UserPublic]): Список пользователей на странице.
        total (int): Общее число пользователей.
        page (int): Номер страницы.
        limit (int): Максимальное количество пользователей на странице.
    """
    items: list[UserPublic]


# параметры запросов
class PaginationParams(BaseModel):
    """Параметры пагинации.
    
    Params:
        page (int): Номер страницы. Не меньше 1. По умолчанию 1.
        limit (int): Максимальное число объектов на странице. Не меньше 1, не
            больше 100. По умолчанию 10.
    """
    page: int = Query(1, ge=1)
    limit: int = Query(10, ge=1, le=100)


class UsersFilterParams(BaseModel):
    """Параметры фильтрации пользователей.
    
    Params:
        id (int | None): ID пользователя или None в случае отсутствия
            фильтрации по данному полю. По умолчанию None.
        username (str | None): Фильтр по содержанию подстроки в имени
            пользователя или None в случае отсутствия фильтрации по данному
            полю. По умолчанию None.
        is_verified (bool | None): Флаг верифицированности или None в случае
            отсутствия фильтрации по данному полю. По умолчанию None.
        is_moderator (bool | None): Флаг, является ли пользователь модератором,
            или None в случае отсутствия фильтрации по данному полю. По
            умолчанию None.
        is_banned (bool | None): Флаг забаненности или None в случае отсутствия
            фильтрации по данному полю. По умолчанию None.
    
    Methods:
        filter_dump: Дамп фильтров в виде списка отдельных условий для WHERE в
            запросе через SQLModel
    """
    id: int | None = Query(None)
    username: str | None = Query(None)
    is_verified: bool | None = Query(None)
    is_moderator: bool | None = Query(None)
    is_banned: bool | None = Query(None)

    @field_validator('username')
    def validate_username_filter(cls, username: str | None) -> str | None:
        """Валидатор поля username (имя пользователя).

        Args:
            username (str | None): Имя пользователя.

        Returns:
            str | None: Имя пользователя.
        """
        return get_valid_username_filter(username)

    def filters_dump(self) -> list[Any]:
        """Дамп фильтров.

        В виде списка отдельных условий для WHERE в запросе через SQLModel.

        Returns:
            list[Any]: Дамп фильтров.
        """
        filters = []
        if self.id is not None:
            filters.append(User.id == self.id)
        if self.is_verified is not None:
            filters.append(User.is_verified == self.is_verified)
        if self.is_moderator is not None:
            filters.append(User.is_moderator == self.is_moderator)
        if self.is_banned is not None:
            filters.append(User.is_banned == self.is_banned)
        if self.username is not None:
            filters.append(col(User.username).contains(self.username,
                                                       autoescape=True))
        return filters
