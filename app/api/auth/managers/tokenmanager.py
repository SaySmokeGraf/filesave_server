"""Менеджер токенов для аут.-авт."""

from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt

from app.api.auth.managers.config import (
    ACCESS_TOKEN_EXPIRE_DAYS, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM,
    PATH_SECRET_USERS
)


_path_secret_users = Path(PATH_SECRET_USERS)


class TokenManager:
    """Менеджер токенов.
    
    Отвечает за взаимодействие с токенами.
    """

    def __init__(self):
        """Инициализация экземпляра менеджера токенов."""
        self._read_key()

    def _read_key(self) -> None:
        """Прочитать ключ шифрования токенов."""
        with open(_path_secret_users, 'r') as file:
            self._key = file.read()

    def create_token(self, data: dict,
                     expires_delta: timedelta | None = None) -> str:
        """Создать токен.

        Args:
            data (dict): Данные для записи в токен.
            expires_delta (timedelta | None): Время истечения токена. По
                умолчанию - None.

        Returns:
            str: Токен.
        """
        to_encode = data.copy()
        if not expires_delta:
            expires_delta = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS,
                                      minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, self._key, algorithm=ALGORITHM)
        return encoded_jwt
    
    def decode_token(self, token: str) -> dict:
        """Расшифровать токен.

        Args:
            token (str): Токен.

        Returns:
            dict: Расшифрованные данные из токена.
        """
        return jwt.decode(token, self._key, algorithms=[ALGORITHM])
