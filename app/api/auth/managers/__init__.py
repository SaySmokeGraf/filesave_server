"""Пакет с менеджерами для API аутентификации-авторизации.

Содержит в себе:
    config - конфигурационный скрипт для менеджеров.
    dbmanager - пакет с менеджером БД.
    tokenmanager - модуль с менеджером токенов.
    usermanager - модуль с менеджером пользователей.

Кроме того:
    token_manager - синглотн менеджера токенов (TokenManager).
    user_manager - синглтон менеджера пользователей (UserManager).
    UserPublic - модель публичных данных пользователя из dbmanager для удобства
        импортирования извне.
"""

from app.api.auth.managers.dbmanager import UserPublic
from app.api.auth.managers.tokenmanager import TokenManager
from app.api.auth.managers.usermanager import UserManager


# экземпляры менеджеров для реализации синглтонов через импортирование
token_manager = TokenManager()
user_manager = UserManager()
