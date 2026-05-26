"""Зависимости для файлового API."""

from typing import Annotated

from fastapi import Depends, HTTPException, status, UploadFile

from app.api.files.utils.validation import (
    isvalid_file_size, isvalid_filename, normalize_filename
)


# зависимости в формате функций
async def validate_single_file(file: UploadFile, rename: bool = False) -> UploadFile:
    """Проверить один файл на соответствие требованиям сервиса.

    Args:
        file (UploadFile): Файл для проверки.
        rename (bool, optional): Флаг переименования в случае небезопасного
            имени. По умолчанию False.
    
    Raises:
        HTTPException: (413) Размер файла слишком велик.
        HTTPException: (400) Если имя небезопасно, при этом параметр rename
            равен False.

    Returns:
        UploadFile: Исходный файл.
    """
    if not isvalid_file_size(file.size):
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail=f'File size is too large'
        )
    
    if rename:
        file.filename = normalize_filename(file.filename)
    else:
        if not isvalid_filename(file.filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Bad filename'
            )
        
    return file


# зависимости в более компактном формате для объявления через аннотирование
SingleFileDep = Annotated[UploadFile, Depends(validate_single_file)]
