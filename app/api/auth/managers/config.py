"""Конфигурационный скрипт для API аут.-авт."""

# пути
PATH_SECRET_USERS = 'app/api/auth/managers/resources/secret_users.txt'

# константы для токена
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_DAYS = 1
ACCESS_TOKEN_EXPIRE_MINUTES = 0

# пароль-"пустышка"
DUMMY_PASSWORD = 'some_dummy_password'
