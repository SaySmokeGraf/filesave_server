"""Зависимости для файлового API.

Dependencies:
    validate_filename: Валидировать имя файла по требованиям сервиса.
    validate_single_file: Проверка одного файла на соответствие требованиям
        сервиса.

AnnotatedDeps:
    FilenameDep (str): Валидировать имя файла по требованиям сервиса.
    SingleFileDep (UploadFile): Проверка одного файла на соответствие
        требованиям сервиса.
"""

from typing import Annotated

from fastapi import Depends, HTTPException, Query, status, UploadFile

import app.api.files._swagger_docs as swdocs
from app.api.files.utils.validation import (
    isvalid_file_size, isvalid_filename, normalize_filename
)


# зависимости в формате функций
async def validate_single_file(
    file: UploadFile,
    rename: bool = Query(default=False, **swdocs.params.rename.docs_dump())
) -> UploadFile:
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

async def validate_filename(filename: str) -> str:
    """Валидировать имя файла по требованиям сервиса.

    Args:
        filename (str): Имя файла.

    Raises:
        HTTPException: (422) Невалидное имя файла.

    Returns:
        str: Имя файла без изменений.
    """
    if not isvalid_filename(filename):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail='Bad filename'
        )
    return filename


# зависимости в более компактном формате для объявления через аннотирование
SingleFileDep = Annotated[UploadFile, Depends(validate_single_file)]
FilenameDep = Annotated[str, Depends(validate_filename)]
