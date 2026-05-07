"""Утилиты для работы с файлами, папками и путями."""

from pathlib import Path
from shutil import copyfileobj

from fastapi import HTTPException, status, UploadFile

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

def set_unique_filename(file: UploadFile, directory_path: Path) -> None:
    """Задать файлу уникальное имя.

    Проверяет в папке наличиче файла с таким же именем, и при наличии онного
    добавляет к нему номер.

    Args:
        file (UploadFile): Файл.
        directory_path (Path): Путь до папки хранения.
    """
    file_path = Path(file.filename)
    cnt = 1
    name, ext, nowname = file_path.stem, file_path.suffix, file_path.name
    while (directory_path / nowname).exists():
        nowname = f'{name} ({cnt}){ext}'
        cnt += 1
    file.filename = nowname

def write_uploadfile(file: UploadFile, directory_path: Path,
                     overwrite: bool | None = None) -> None:
    """Записать UploadFile в файл.

    Args:
        file (UploadFile): UploadFile для записи.
        directory_path (Path): Путь до директории для записи файла.
        overwrite (bool | None): Флаг перезаписи файла в случае наличия файла
            с таким же именем в хранилище. True - перезаписать, False - создать
            уникальное имя с помощью суффикса с номером, None - откинуть
            ошибку. По умолчанию None.
    
    Raises:
        HTTPException: Если файл с таким именем есть в хранилище, но нет
            указаний на этот случай во флаге overwrite.
    """
    if overwrite is None and (directory_path / file.filename).exists():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'File {file.filename} already exists'
        )
    if overwrite == False:
        set_unique_filename(file, directory_path)
    file_path = directory_path / file.filename
    with open(file_path, "wb") as buffer:
        copyfileobj(file.file, buffer)
