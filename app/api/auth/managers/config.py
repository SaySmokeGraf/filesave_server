"""Конфигурационный скрипт для API аутентификации-авторизации.

Consts:
    ACCESS_TOKEN_EXPIRE_DAYS (int): Дни действия токена.
    ACCESS_TOKEN_EXPIRE_MINUTES (int): Минуты действия токена.
    PATH_SECRET_USERS (str): Путь до соли JWT-токенов.
    ALGORITHM (str): Алгоритм шифрования токенов.
    DUMMY_PASSWORD (str): Пароль-"пустышка" для использования в защите от
        time-related атак.
"""

from app.settings import (
    ACCESS_TOKEN_EXPIRE_DAYS, ACCESS_TOKEN_EXPIRE_MINUTES, PATH_SECRET_USERS
)


# константы для токена
ALGORITHM = 'HS256'

# пароль-"пустышка"
DUMMY_PASSWORD = 'some_dummy_password'
