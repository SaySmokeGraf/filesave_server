"""Утилиты для работы аутентификации-авторизации."""

import re
import unicodedata

from fastapi import HTTPException, status


# константы
_MIN_USERNAME_LENGTH = 4
_MAX_USERNAME_LENGTH = 64
_MIN_PWD_LENGTH = 4
_MAX_PWD_LENGTH = 128

_REPLACEMENT_CHAR = ''
_REGEX_UNSAFE_USERNAME_CHARS = r'[^A-Za-z0-9._\-]'
_REGEX_UNSAFE_PWD_CHARS = r'[^A-Za-z0-9._\-!@#$%\^&*()\[\]+={};:\'\",<>/\\?|~]'


# валидация
def validate_username(username: str) -> None:
    """Валидировать имя пользователя.

    Args:
        username (str): Имя пользователя.

    Raises:
        HTTPException: (422) Невалидное имя.
    """
    invalid_username_exception = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        detail='Invalid username',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    # исправление небезопасных символов
    nowname = unicodedata.normalize('NFKC', username)
    nowname = ''.join(
        char for char in nowname
        if unicodedata.category(char)[0] != 'C'
    )
    nowname = nowname.strip()
    nowname = re.sub(_REGEX_UNSAFE_USERNAME_CHARS, _REPLACEMENT_CHAR, nowname,
                     flags=re.UNICODE)
    if nowname != username:
        raise invalid_username_exception
    
    # ограничение длины
    if len(username) > _MAX_USERNAME_LENGTH or len(username) < _MIN_USERNAME_LENGTH:
        raise invalid_username_exception

def validate_password(password: str) -> None:
    """Валидировать пароль.

    Args:
        password (str): Пароль.

    Raises:
        HTTPException: (422) Невалидный пароль.
    """
    invalid_pwd_exception = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        detail='Invalid password',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    # исправление небезопасных символов
    nowpwd = unicodedata.normalize('NFKC', password)
    nowpwd = ''.join(
        char for char in nowpwd
        if unicodedata.category(char)[0] != 'C'
    )
    nowpwd = nowpwd.strip()
    nowpwd = re.sub(_REGEX_UNSAFE_PWD_CHARS, _REPLACEMENT_CHAR, nowpwd,
                     flags=re.UNICODE)
    if nowpwd != password:
        raise invalid_pwd_exception
    
    # ограничение длины
    if len(password) > _MAX_PWD_LENGTH or len(password) < _MIN_PWD_LENGTH:
        raise invalid_pwd_exception
