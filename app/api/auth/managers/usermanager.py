"""Менеджер данных по безопасности для аут.-авт."""

from pwdlib import PasswordHash

from app.api.auth.models import UserInDB
from app.api.auth.managers.config import DUMMY_PASSWORD, PATH_DB
from app.api.auth.managers.dbmanager import DBManager


class UserManager:
    def __init__(self):
        self._pwd_hasher = PasswordHash.recommended()
        self._db_manager = DBManager(PATH_DB)

        self._DUMMY_HASH = self._pwd_hasher.hash(DUMMY_PASSWORD)
    
    def authenticate_user(self, username: str, password: str):
        user = self._db_manager.get_user(username)
        if not user:
            self._pwd_hasher.verify(password, self._DUMMY_HASH)
            return False
        if not self._pwd_hasher.verify(password, user.hashed_password):
            return False
        return user
    
    def get_user(self, username: str) -> UserInDB:
        return self._db_manager.get_user(username)

    def save_user(self, username: str, password: str):
        user = UserInDB(
            username=username,
            hashed_password=self._pwd_hasher.hash(password)
        )
        self._db_manager.add_user(user)
