"""Роутер под файловый API."""

import os

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse

from app.api.files.config import PATH_STORAGE
from app.api.files.dependencies import ManyFilesDep, SingleFileDep
from app.api.files.models import FileDataModel
from app.api.files.utils import write_uploadfile


router = APIRouter()


@router.get('/', response_model=list[FileDataModel])
async def get_files_data() -> list[FileDataModel]:
    """Получить список с данными о файлах.

    Raises:
        HTTPException: Произошли изменения в папке во время работы.

    Returns:
        list[FileDataModel]: Список с данными о файлах.
    """
    resp = []
    dir_path = PATH_STORAGE
    try:
        for filename in os.listdir(dir_path):
            resp.append(FileDataModel(
                filename=filename,
                size=os.path.getsize(f'{dir_path}/{filename}')
            ))
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Storage or file moved while working'
        )
    return resp

@router.get('/download')
async def download_file(filename: str) -> FileResponse:
    """Скачать файл.

    Args:
        filename (str): Имя файла.

    Raises:
        HTTPException: Файла с таким именем нет.

    Returns:
        FileResponse: Файл для скачивания.
    """
    dir_path = PATH_STORAGE
    file_path = f'{dir_path}/{filename}'
    if not filename or not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'File {filename} not found'
        )
    return FileResponse(path=file_path, filename=filename)

@router.post('/upload/single', status_code=status.HTTP_201_CREATED)
async def upload_single_file(file: SingleFileDep) -> JSONResponse:
    """Загрузить на сервер один файл.

    Args:
        file (UploadFile): Файл для загрузки.

    Returns:
        JSONResponse: Ответ об успешном выполнении.
    """
    dir_path = PATH_STORAGE
    write_uploadfile(file, dir_path)
    return JSONResponse(
        content={'message': f'File {file.filename} uploaded successfully!'}
    )

@router.post('/upload/many', status_code=status.HTTP_201_CREATED)
async def upload_many_files(files: ManyFilesDep) -> JSONResponse:
    """Загрузить на сервер несколько файлов.

    Args:
        files (list[UploadFile]): Список файлов.

    Returns:
        JSONResponse: Ответ об успешном выполнении.
    """
    dir_path = PATH_STORAGE
    for file in files:
        write_uploadfile(file, dir_path)
    return JSONResponse(
        content={'message': 'Files uploaded successfully!'}
    )

@router.delete('/delete')
async def delete_file(filename: str) -> JSONResponse:
    """Удалить файл с сервера.

    Args:
        filename (str): Имя файла.

    Raises:
        HTTPException: Файла с таким именем нет.
        HTTPException: Нет доступа для удаления (например, файл занят другим процессом).

    Returns:
        JSONResponse: Ответ об успешном выполнении.
    """
    dir_path = PATH_STORAGE
    file_path = f'{dir_path}/{filename}'
    if not filename or not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'File {filename} not found'
        )
    try:
        os.remove(file_path)
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='No permissions to delete'
        )
    return JSONResponse(
        content={'message': f'File {filename} deleted successfully!'}
    )
