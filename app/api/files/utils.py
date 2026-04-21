"""Утилиты для файлового API."""

import os
from shutil import copyfileobj

from fastapi import UploadFile

from app.api.files.config import PATH_STORAGE


def get_user_dir_path(user_dir: str) -> str:
    """Получить путь до папки пользователя.

    Проверяет ее существование и создает, если папки нет.

    Args:
        user_dir (str): Имя папки пользователя.

    Returns:
        str: Путь до папки пользователя.
    """
    dir_path = f'{PATH_STORAGE}/{user_dir}'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def get_unique_filename(filename: str, directory_path: str) -> str:
    """Получить уникальное имя файла.

    Проверяет в папке наличиче файла с таким же именем, и при наличии
    онного добавляет к нему номер.

    Args:
        filename (str): Имя файла.
        directory_path (str): Путь до папки хранения.

    Returns:
        str: Уникальное имя файла.
    """
    base, ext = os.path.splitext(filename)
    cnt = 1
    nowname = filename
    while os.path.exists(f'{directory_path}/{nowname}'):
        nowname = f'{base} ({cnt}){ext}'
        cnt += 1
    return nowname

def write_uploadfile(file: UploadFile, directory_path: str,
                     overwrite: bool = False) -> None:
    """Записать UploadFile в файл.

    Args:
        file (UploadFile): UploadFile для записи.
        directory_path (str): Путь до директории для записи файла.
        overwrite (bool): Флаг перезаписи файла в случае совпадения
            имен. По умолчанию False.
    """
    if overwrite:
        filename = file.filename
    else:
        filename = get_unique_filename(file.filename, directory_path)
    file_path = f'{directory_path}/{filename}'
    with open(file_path, "wb") as buffer:
        copyfileobj(file.file, buffer)
