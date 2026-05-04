"""Конфигурационный скрипт для менеджера БД."""

# пути
PATH_DB_DIR = 'app/api/auth/managers/dbmanager/resources'
PATH_DB = f'{PATH_DB_DIR}/users.db'

# url бд
SQLITE_URL = f'sqlite:///{PATH_DB}'
