"""Менеджер токенов для API авт.-аут."""

from datetime import datetime, timedelta, timezone

import jwt

from app.api.auth.managers.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, PATH_SECRET_USERS
) 


class TokenManager:
    def __init__(self):
        self._read_key()

    def _read_key(self):
        with open(PATH_SECRET_USERS, 'r') as file:
            self._key = file.read()

    def create_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, self._key, algorithm=ALGORITHM)
        return encoded_jwt
    
    def decode_token(self, token: str):
        return jwt.decode(token, self._key, algorithms=[ALGORITHM])
