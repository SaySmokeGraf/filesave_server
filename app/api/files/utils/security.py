"""Функции, связанные с безопасностью при работе с файлами."""

import re
import unicodedata
from pathlib import Path
from shutil import disk_usage

from fastapi import HTTPException, status, UploadFile

from app.api.files.config import PATH_DISK, RESERVED_DISK_SPACE


# вспомогательные переменные и константы
_path_disk = Path(PATH_DISK)

_WINDOWS_RESERVED = {
    'CON', 'PRN', 'AUX', 'NUL',
    *(f'COM{i}' for i in range(1, 10)),
    *(f'LPT{i}' for i in range(1, 10))
}

_FILE_NAME_MAX_LENGTH = 200
_FILE_EXT_MAX_LENGTH = 50

_REPLACEMENT_CHAR = '_'
_REGEX_UNSAFE_NAME_CHARS = r'[^\w\-_.\d\s(){}\[\]]'
_REGEX_UNSAFE_EXT_CHARS = r'[^A-Za-z\-_.\d]'


# вспомогательные функции
def _make_safe_filename(filename: str) -> str:
    """Сделать безопасное имя файла.

    Args:
        filename (str): Имя файла.

    Returns:
        str: Безопасное имя файла.
    """
    # исправление полного имени от path traversal и unicode-related атак
    filename = Path(filename).name
    filename = unicodedata.normalize('NFKC', filename)
    filename = ''.join(
        char for char in filename
        if unicodedata.category(char)[0] != 'C'
    )

    if '.' in filename:
        name, ext = filename.rsplit('.', 1)
        ext = '.' + ext
    else:
        name = filename
        ext = ''

    # исправление небезопасных символов
    ext = ext.rstrip()
    name = re.sub(_REGEX_UNSAFE_NAME_CHARS, _REPLACEMENT_CHAR, name,
                  flags=re.UNICODE)
    ext = re.sub(_REGEX_UNSAFE_EXT_CHARS, _REPLACEMENT_CHAR, ext,
                 flags=re.UNICODE)
    name = name.strip('. ')
    

    # проверка на зарезервированные имена
    if name.upper() in _WINDOWS_RESERVED:
        name = f'_{name}'
    
    # ограничение длины
    if len(name) > _FILE_NAME_MAX_LENGTH:
        name = name[:_FILE_NAME_MAX_LENGTH]
    if len(ext) > _FILE_EXT_MAX_LENGTH:
        ext = ext[:_FILE_EXT_MAX_LENGTH]

    # если имя пустое
    if not name:
        name = 'unnamed'

    return name + ext


# проверки файлов и их параметров
def check_file_size(size: int) -> None:
    """Проверить размер файла и свободное место на диске.

    Args:
        size (int): Размер файла.

    Raises:
        HTTPException: Размер файла слишком велик.
    """
    free_space = disk_usage(_path_disk).free - RESERVED_DISK_SPACE
    if size > free_space:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Files total size is too large'
        )

def check_filename(file: UploadFile, rename: bool = False) -> None:
    """Проверить имя файла на безопасность.

    Имеет флаг переименования в случае небезопасного имени.

    Args:
        filename (str): Имя файла.
        rename (bool): Флаг переименования в случае небезопасного имени. По
            умолчанию False.

    Raises:
        HTTPException: Если имя небезопасно, при этом параметр rename равен
            False.
    """
    filename = file.filename
    safe_filename = _make_safe_filename(filename)
    if rename:
        file.filename = safe_filename
        return
    elif filename != safe_filename:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Bad filename'
        )
