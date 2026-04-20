"""Конфигурационный скрипт для менеджера БД."""

# пути
PATH_DB = 'app/api/auth/managers/dbmanager/resources/users.db'

# url бд
SQLITE_URL = f'sqlite:///{PATH_DB}'


# константы
class RoleToID:
    """ID ролей."""
    UNVERIFIED = 0
    USER = 1
    REJECTED = 2
    ADMIN = 3
