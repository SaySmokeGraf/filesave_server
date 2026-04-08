"""Модели для файлового API."""

from pydantic import BaseModel


class FileDataModel(BaseModel):
    """Модель данных о файле.

    Args:
        filename (str): Имя файла.
        size (int): Размер файла в байтах.
    """
    filename: str
    size: int
