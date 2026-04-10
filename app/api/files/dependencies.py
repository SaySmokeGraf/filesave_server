"""Зависимости для файлового API."""

from shutil import disk_usage
from typing import Annotated

from fastapi import Depends, HTTPException, status, UploadFile

from app.api.files.config import PATH_DISK, RESERVED_DISK_SPACE


# вспомогательные
def _check_size(size: int):
    """Проверить размер файла(ов) и свободное место на диске.

    Args:
        size (int): Размер файла(ов).

    Raises:
        HTTPException: Размер файла(ов) слишком велик.
    """
    free_space = disk_usage(PATH_DISK).free - RESERVED_DISK_SPACE
    if size > free_space:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Files total size is too large'
        )


# зависимости в формате функций
async def validate_single_file(file: UploadFile) -> UploadFile:
    """Проверить один файл на соответствие требованиям сервиса.

    Косвенно вызывает HTTPException в случае несоответствия.

    Args:
        file (UploadFile): Файл для проверки.

    Returns:
        UploadFile: Исходный файл.
    """
    _check_size(file.size)
    return file

async def validate_many_files(files: list[UploadFile]) -> list[UploadFile]:
    """Проверить список файлов на соответствие требованиям сервиса.

    Косвенно вызывает HTTPException в случае несоответствия.

    Args:
        files (list[UploadFile]): Список файлов для проверки.

    Returns:
        list[UploadFile]: Исходный список файлов.
    """
    _check_size(sum([file.size for file in files]))
    return files


# зависимости в более компактном формате для объявления через аннотирование
SingleFileDep = Annotated[UploadFile, Depends(validate_single_file)]
ManyFilesDep = Annotated[list[UploadFile], Depends(validate_many_files)]
