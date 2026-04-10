"""Менеджер БД для API авто.-аут."""

from app.api.auth.models import UserInDB


DELIMITER = ' '


class DBManager:
    def __init__(self, path: str):
        self._path = path
        self._read_fake_db()
    
    def _read_fake_db(self):
        self._db_data = dict()
        with open(self._path, 'r') as db:
            for line in db.readlines():
                if line:
                    line = line.rstrip('\n').split(DELIMITER)
                    self._db_data[line[0]] = line[1]
    
    def _save_db(self):
        with open(self._path, 'w') as db:
            for key in self._db_data:
                db.write(f'{key}{DELIMITER}{self._db_data[key]}\n')
    
    def get_user(self, username: str) -> UserInDB:
        if username not in self._db_data:
            return None
        return UserInDB(username=username, hashed_password=self._db_data[username])
    
    def add_user(self, user: UserInDB) -> None:
        self._db_data[user.username] = user.hashed_password
        self._save_db()
