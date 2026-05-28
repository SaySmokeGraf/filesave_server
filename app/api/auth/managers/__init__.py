"""Пакет с менеджерами для API аутентификации-авторизации.

Contains:
    config: Конфигурационный скрипт для менеджеров.
    dbmanager: Пакет с менеджером БД.
    tokenmanager: Модуль с менеджером токенов.
    usermanager: Модуль с менеджером пользователей.

Singletons:
    token_manager (TokenManager): Менеджер токенов .
    user_manager (UserManager): Менеджер пользователей.

Models:
    Некоторые модели из пакета dbmanager для удобства импортирования.
"""

from app.api.auth.managers.dbmanager import (
    PagedUsersPublic, UserPublic, PaginationParams, UsersFilterParams,
    UserUpdateRights
)
from app.api.auth.managers.tokenmanager import TokenManager
from app.api.auth.managers.usermanager import UserManager


# экземпляры менеджеров для реализации синглтонов через импортирование
token_manager = TokenManager()
user_manager = UserManager()
