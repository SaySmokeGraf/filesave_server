"""Роутер под файловый API."""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse

from app.api.auth.dependencies import GetUserDirectoryDep
from app.api.files.dependencies import SingleFileDep
from app.api.files.models import FileDataModel
from app.api.files.utils.file_utils import (
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
    for file_path in dir_path.iterdir():
        resp.append(FileDataModel(
            filename=file_path.name,
            size=file_path.stat().st_size
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
    file_path = dir_path / filename
    if not filename or not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'File {filename} not found'
        )
    return FileResponse(path=file_path, filename=filename)

@router.post('/upload/single', status_code=status.HTTP_201_CREATED)
async def upload_single_file(file: SingleFileDep,
                             user_dir: GetUserDirectoryDep,
                             overwrite: bool | None = None) -> JSONResponse:
    """Загрузить на сервер один файл.

    Args:
        file (SingleFileDep): Файл для загрузки.
        user_dir (GetUserDirectoryDep): Имя папки пользователя.
        overwrite (bool | None): Флаг перезаписи файла в случае наличия файла
            с таким же именем в хранилище. True - перезаписать, False - создать
            уникальное имя с помощью суффикса с номером, None - откинуть
            ошибку. По умолчанию None.

    Returns:
        JSONResponse: Ответ об успешном выполнении.
    """
    dir_path = get_user_dir_path(user_dir)
    write_uploadfile(file, dir_path, overwrite)
    return JSONResponse(
        content={'message': f'File {file.filename} uploaded successfully!'}
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
    file_path = dir_path / filename
    if not filename or not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'File {filename} not found'
        )
    try:
        file_path.unlink()
    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='No permissions to delete'
        )
    return JSONResponse(
        content={'message': f'File {filename} deleted successfully!'}
    )
