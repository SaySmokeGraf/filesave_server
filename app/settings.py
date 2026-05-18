"""Скрипт настроек приложения."""

# ********** AUTH **********

# путь до ключа шифрования JWT
PATH_SECRET_USERS = 'app/api/auth/managers/resources/secret_users.txt'

# время истечения токена JWT
ACCESS_TOKEN_EXPIRE_DAYS = 1        # [дни]
ACCESS_TOKEN_EXPIRE_MINUTES = 0     # [минуты]

# путь до папки с БД пользователей и имя файла БД
PATH_DB_DIR = 'app/api/auth/managers/dbmanager/resources'
DB_FILENAME = 'users.db'

# ********** FILES *********

# путь до хранилища файлов пользователей
PATH_STORAGE = 'app/api/files/storage'

# путь диска (корня) с хранилищем для проверки свободного места
PATH_DISK = 'C:'

# зарезервированное место в хранилище
RESERVED_DISK_SPACE = 0             # [байты]

# максимальный размер файла
MAX_FILE_SIZE = 1 << 30             # [байты]
