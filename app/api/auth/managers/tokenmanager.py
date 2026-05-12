"""Менеджер токенов для аут.-авт."""

from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Generator

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
        pass

    @contextmanager
    def _read_key(self) -> Generator[str, None, None]:
        """Прочитать ключ шифрования токенов.

        Yields:
            Generator[str, None, None]: Ключ шифрования.
        """
        file = open(_path_secret_users, 'r')
        try:
            yield file.read()
        finally:
            file.close()

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
        with self._read_key() as key:
            encoded_jwt = jwt.encode(to_encode, key, algorithm=ALGORITHM)
        return encoded_jwt
    
    def decode_token(self, token: str) -> dict:
        """Расшифровать токен.

        Args:
            token (str): Токен.

        Returns:
            dict: Расшифрованные данные из токена.
        """
        with self._read_key() as key:
            decoded_jwt = jwt.decode(token, key, algorithms=[ALGORITHM])
        return decoded_jwt
