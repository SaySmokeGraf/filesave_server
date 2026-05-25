"""Конфигурационный скрипт для API аут.-авт."""

from app.settings import (
    ACCESS_TOKEN_EXPIRE_DAYS, ACCESS_TOKEN_EXPIRE_MINUTES, PATH_SECRET_USERS
)


# константы для токена
ALGORITHM = 'HS256'

# пароль-"пустышка"
DUMMY_PASSWORD = 'some_dummy_password'
