"""Утилиты для файлового API."""

from shutil import copyfileobj

from fastapi import UploadFile


def write_uploadfile(file: UploadFile, directory_path: str) -> None:
    """Записать UploadFile в файл.

    Args:
        file (UploadFile): UploadFile для записи.
        directory_path (str): Путь до директории для записи файла.
    """
    file_path = f'{directory_path}/{file.filename}'
    with open(file_path, "wb") as buffer:
        copyfileobj(file.file, buffer)
