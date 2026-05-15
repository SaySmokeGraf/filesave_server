"""Отдельные шаги валидации или нормализации полей."""

import re
import unicodedata
from pathlib import Path

from app.api.utils.validation.config import (
    REPLACEMENT_CHAR, UNNAMED_REPLACEMENT, WINDOWS_RESERVED
)


# вспомогательные
SplittedFilename = tuple[str, str]

def split_filename(filename: str) -> SplittedFilename:
    """Разделить имя файла на имя (стэм) и расширение.

    Args:
        filename (str): Имя файла.

    Returns:
        SplittedFilename: Имя и расширение.
    """
    filename_path = Path(filename)
    return filename_path.stem, filename_path.suffix

def build_filename(name: str, ext: str) -> str:
    """Собрать имя файла из имени (стэма) и расширения.

    Args:
        name (str): Имя (стэм).
        ext (str): Расширение.

    Returns:
        str: Имя файла.
    """
    return name + ext


# нормализация
def normalize_path_traversal(filename: str) -> str:
    """Нормализовать имя файла от path traversal.

    Args:
        filename (str): Имя файла.

    Returns:
        str: Нормализованное имя файла.
    """
    return Path(filename).name

def normalize_unicode(field: str) -> str:
    """Нормализовать поле по юникоду.

    Args:
        field (str): Поле для нормализации.

    Returns:
        str: Нормализованное поле.
    """
    field = unicodedata.normalize('NFKC', field)
    field = ''.join(
        char for char in field
        if unicodedata.category(char)[0] != 'C'
    )
    return field

def normalize_chars(field: str, unsafe_chars: str) -> str:
    """Нормализовать символы поля по запрещенным символам.

    Заменяет символы на REPLACEMENT_CHAR.

    Args:
        field (str): Поле для нормализации.
        unsafe_chars (str): Регулярное выражение для небезопасных символов.

    Returns:
        str: Нормализованное поле.
    """
    field = field.strip()
    field = re.sub(unsafe_chars, REPLACEMENT_CHAR, field, flags=re.UNICODE)
    return field

def normalize_reserved_names(name: str) -> str:
    """Нормализовать имя (стэм) файла по зарезервированным именам.

    Args:
        name (str): Имя (стэм).

    Returns:
        str: Нормализованное имя (стэм).
    """
    if name.upper() in WINDOWS_RESERVED:
        return f'_{name}'
    return name

def normalize_length(field: str, max_len: int, cut_left: bool = False) -> str:
    """Нормализовать поле по длине.

    Args:
        field (str): Поле для нормализации.
        max_len (int): Максимальная длина поля.
        cut_left (bool, optional): Флаг срезания символов слева (с начала), а
            не справа (с конца). По умолчанию False.

    Returns:
        str: Нормализованное поле.
    """
    if len(field) > max_len:
        return field[:max_len] if not cut_left else field[-max_len:]
    return field

def normalize_empty_name(name: str) -> str:
    """Нормализовать имя (стэм) по пустому имени.

    Заменяет пустое имя на UNNAMED_REPLACEMENT.

    Args:
        name (str): Имя (стэм).

    Returns:
        str: Нормализованное имя (стэм).
    """
    if not name:
        return UNNAMED_REPLACEMENT
    return name


# валидация
def isvalid_path_traversal(filename: str) -> bool:
    """Проверка валидности имени файла по path traversal.

    Args:
        filename (str): Имя файла.

    Returns:
        bool: Валидность.
    """
    return filename == normalize_path_traversal(filename)

def isvalid_reserved_names(name: str) -> bool:
    """Проверка валидности имени (стэма) по зарезервированным именам.

    Args:
        name (str): Имя (стэм).

    Returns:
        bool: Валидность.
    """
    return name.upper() not in WINDOWS_RESERVED

def isvalid_length(field: str, min_len: int = 0, max_len: int = 0) -> bool:
    """Проверка валидности по длине поля.

    Args:
        field (str): Поле для валидации.
        min_len (int, optional): Минимальная длина. По умолчанию 0.
        max_len (int, optional): Максимальная длина. По умолчанию 0.

    Returns:
        bool: Валидность.
    """
    return min_len <= len(field) <= max_len

def isvalid_unicode(field: str) -> bool:
    """Проверка валидности поля по юникоду.

    Args:
        field (str): Поле для валидации.

    Returns:
        bool: Валидность.
    """
    return field == normalize_unicode(field)

def isvalid_chars(field: str, unsafe_chars: str) -> str:
    """Проверка валидности поля по символам.

    Args:
        field (str): Поле для валидации.
        unsafe_chars (str): Регулярное выражение небезопасных символов.

    Returns:
        str: Валидность.
    """
    if not field:
        return True
    return field.strip() == field and re.search(unsafe_chars, field) is None
