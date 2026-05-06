"""Утилиты для работы с файлами, папками и путями."""

from pathlib import Path
from shutil import copyfileobj

from fastapi import UploadFile

from app.api.files.config import PATH_STORAGE


_path_storage = Path(PATH_STORAGE)


def create_storage_directory() -> None:
    """Создать папку хранилища, если нужно."""
    if not _path_storage.exists():
        _path_storage.mkdir(parents=True)

def get_user_dir_path(user_dir: str) -> Path:
    """Получить путь до папки пользователя.

    Проверяет ее существование и создает, если папки нет.

    Args:
        user_dir (str): Имя папки пользователя.

    Returns:
        Path: Путь до папки пользователя.
    """
    dir_path = _path_storage / user_dir
    if not dir_path.exists():
        dir_path.mkdir()
    return dir_path

def get_unique_filename(filename: str, directory_path: Path) -> str:
    """Получить уникальное имя файла.

    Проверяет в папке наличиче файла с таким же именем, и при наличии
    онного добавляет к нему номер.

    Args:
        filename (str): Имя файла.
        directory_path (Path): Путь до папки хранения.

    Returns:
        str: Уникальное имя файла.
    """
    file = Path(filename)
    cnt = 1
    nowname = filename
    while (directory_path / nowname).exists():
        nowname = f'{file.stem} ({cnt}){file.suffix}'
        cnt += 1
    return nowname

def write_uploadfile(file: UploadFile, directory_path: Path,
                     overwrite: bool = False) -> None:
    """Записать UploadFile в файл.

    Args:
        file (UploadFile): UploadFile для записи.
        directory_path (Path): Путь до директории для записи файла.
        overwrite (bool): Флаг перезаписи файла в случае совпадения
            имен. По умолчанию False.
    """
    if overwrite:
        filename = file.filename
    else:
        filename = get_unique_filename(file.filename, directory_path)
        file.filename = filename
    file_path = directory_path / filename
    with open(file_path, "wb") as buffer:
        copyfileobj(file.file, buffer)
