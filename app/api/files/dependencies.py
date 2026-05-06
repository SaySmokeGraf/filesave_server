"""Зависимости для файлового API."""

from typing import Annotated

from fastapi import Depends, UploadFile

from app.api.files.utils.security import check_file_size, check_filename


# зависимости в формате функций
async def validate_single_file(file: UploadFile, rename: bool = False) -> UploadFile:
    """Проверить один файл на соответствие требованиям сервиса.

    Косвенно вызывает HTTPException в случае несоответствия.

    Args:
        file (UploadFile): Файл для проверки.

    Returns:
        UploadFile: Исходный файл.
    """
    check_file_size(file.size)
    check_filename(file, rename)
    return file


# зависимости в более компактном формате для объявления через аннотирование
SingleFileDep = Annotated[UploadFile, Depends(validate_single_file)]
