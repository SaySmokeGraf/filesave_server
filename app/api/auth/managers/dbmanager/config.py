"""Конфигурационный скрипт для менеджера БД."""

from app.settings import DB_FILENAME, PATH_DB_DIR


# пути
PATH_DB = f'{PATH_DB_DIR}/{DB_FILENAME}'

# url бд
SQLITE_URL = f'sqlite:///{PATH_DB}'
