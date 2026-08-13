"""Пакет с менеджером БД для API аутентификации-авторизации.

Contains:
    config: Конфигурационный скрипт для менеджера БД.
    dbmanager: Модуль с менеджером БД.
    models: Модуль с моделями для менеджера БД и моделями пользователей для
        использования вовне.
    validation: Модуль с валидациями для менеджера БД.

Classes:
    DBManager: dbmanager.DBManager для удобства импортирования.

Models:
    Некоторые модели данных из модуля models для удобства импортирования.
"""

from app.api.auth.managers.dbmanager.dbmanager import DBManager
from app.api.auth.managers.dbmanager.models import (
    User, UserCreate, UserPublic, UserUpdateRights,
    AbstractPagedItems, PagedUsers, PagedUsersPublic,
    PaginationParams, UsersFilterParams
)
