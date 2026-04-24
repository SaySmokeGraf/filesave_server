"""Роутер под файловый API."""

import os

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse

from app.api.auth.dependencies import GetUserDirectoryDep
from app.api.files.dependencies import ManyFilesDep, SingleFileDep
from app.api.files.models import FileDataModel
from app.api.files.utils import (
    create_storage_directory, get_user_dir_path, write_uploadfile
)


router = APIRouter()
create_storage_directory()


@router.get('/', response_model=list[FileDataModel])
async def get_files_data(user_dir: GetUserDirectoryDep) -> list[FileDataModel]:
    """Получить список с данными о файлах.

    Args:
        user_dir (GetUserDirectoryDep): Имя папки пользователя.

    Returns:
        list[FileDataModel]: Список с данными о файлах.
    """
    resp = []
    dir_path = get_user_dir_path(user_dir)
    for filename in os.listdir(dir_path):
        resp.append(FileDataModel(
            filename=filename,
            size=os.path.getsize(f'{dir_path}/{filename}')
        ))
    return resp

@router.get('/download')
async def download_file(filename: str,
                        user_dir: GetUserDirectoryDep) -> FileResponse:
    """Скачать файл.

    Args:
        filename (str): Имя файла.
        user_dir (GetUserDirectoryDep): Имя папки пользователя.

    Raises:
        HTTPException: Файла с таким именем нет.

    Returns:
        FileResponse: Файл для скачивания.
    """
    dir_path = get_user_dir_path(user_dir)
    file_path = f'{dir_path}/{filename}'
    if not filename or not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'File {filename} not found'
        )
    return FileResponse(path=file_path, filename=filename)

@router.post('/upload/single', status_code=status.HTTP_201_CREATED)
async def upload_single_file(file: SingleFileDep,
                             user_dir: GetUserDirectoryDep,
                             overwrite: bool = False) -> JSONResponse:
    """Загрузить на сервер один файл.

    Args:
        file (SingleFileDep): Файл для загрузки.
        user_dir (GetUserDirectoryDep): Имя папки пользователя.
        overwrite (bool): Флаг перезаписи файла в случае совпадения
            имен. По умолчанию False.

    Returns:
        JSONResponse: Ответ об успешном выполнении.
    """
    dir_path = get_user_dir_path(user_dir)
    write_uploadfile(file, dir_path, overwrite)
    return JSONResponse(
        content={'message': f'File {file.filename} uploaded successfully!'}
    )

@router.post('/upload/many', status_code=status.HTTP_201_CREATED)
async def upload_many_files(files: ManyFilesDep,
                            user_dir: GetUserDirectoryDep,
                            overwrite: bool = False) -> JSONResponse:
    """Загрузить на сервер несколько файлов.

    Args:
        files (list[UploadFile]): Список файлов.
        user_dir (GetUserDirectoryDep): Имя папки пользователя.
        overwrite (bool): Флаг перезаписи файла в случае совпадения
            имен. По умолчанию False.

    Returns:
        JSONResponse: Ответ об успешном выполнении.
    """
    dir_path = get_user_dir_path(user_dir)
    for file in files:
        write_uploadfile(file, dir_path, overwrite)
    return JSONResponse(
        content={'message': 'Files uploaded successfully!'}
    )

@router.delete('/delete')
async def delete_file(filename: str,
                      user_dir: GetUserDirectoryDep) -> JSONResponse:
    """Удалить файл с сервера.

    Args:
        filename (str): Имя файла.
        user_dir (GetUserDirectoryDep): Имя папки пользователя.

    Raises:
        HTTPException: Файла с таким именем нет.
        HTTPException: Нет доступа для удаления (например, файл занят другим процессом).

    Returns:
        JSONResponse: Ответ об успешном выполнении.
    """
    dir_path = get_user_dir_path(user_dir)
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
