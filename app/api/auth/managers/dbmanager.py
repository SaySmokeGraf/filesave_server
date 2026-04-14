"""Менеджер БД для аут.-авт."""

from app.api.auth.managers.config import PATH_DB
from app.api.auth.models import UserInDB


DELIMITER = ' '


class DBManager:
    """Менеджер БД.
    
    Отвечает за все взаимодействия с БД пользователей.
    """

    def __init__(self):
        """Инициализация экземпляра менеджера БД."""
        self._path = PATH_DB
        self._read_fake_db()
    
    def _read_fake_db(self) -> None:
        """Прочитать фейковую БД."""
        self._db_data = dict()
        with open(self._path, 'r') as db:
            for line in db.readlines():
                if line:
                    line = line.rstrip('\n').split(DELIMITER)
                    self._db_data[line[0]] = line[1]
    
    def _save_db(self) -> None:
        """Сохранить БД."""
        with open(self._path, 'w') as db:
            for key in self._db_data:
                db.write(f'{key}{DELIMITER}{self._db_data[key]}\n')
    
    def get_user(self, username: str) -> UserInDB | None:
        """Получить данные о пользователе по логину.

        Args:
            username (str): Логин.

        Returns:
            UserInDB | None: Данные о пользователе или None в случае отсутствия
                онного в БД.
        """
        if username not in self._db_data:
            return None
        return UserInDB(username=username, hashed_password=self._db_data[username])
    
    def add_user(self, user: UserInDB) -> None:
        """Добавить пользователя в БД.

        Args:
            user (UserInDB): Данные о пользователе.
        """
        self._db_data[user.username] = user.hashed_password
        self._save_db()
