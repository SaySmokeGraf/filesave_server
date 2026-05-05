"""Пакет с менеджером БД для API аутентификации-авторизации.

Содержит в себе:
    config - конфигурационный скрипт для менеджера БД.
    dbmanager - модуль с менеджером БД.
    models - модуль с моделями для менеджера БД и моделями пользователей для
        использования вовне.

Кроме того, для удобства импортирования содержит в себе:
    DBManager - dbmanager.DBManager
    User - models.User
    UserCreate - models.UserCreate
    UserPublic - models.UserPublic
"""

from app.api.auth.managers.dbmanager.dbmanager import DBManager
from app.api.auth.managers.dbmanager.models import (
    User, UserCreate, UserPublic
)
