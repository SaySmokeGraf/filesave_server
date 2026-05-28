"""Конфигурационный скрипт для менеджера БД.

Consts:
    PATH_DB (str): Путь до БД.
    SQLITE_URL (str): URL БД для подключения через ORM.
"""

from app.settings import DB_FILENAME, PATH_DB_DIR


# пути
PATH_DB = f'{PATH_DB_DIR}/{DB_FILENAME}'

# url бд
SQLITE_URL = f'sqlite:///{PATH_DB}'
