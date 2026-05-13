"""Модели для файлового API."""

from pydantic import BaseModel


class _BaseFileInfo(BaseModel):
    """Базовая модель информации о файле.

    Params:
        filename (str): Имя файла.
        size (int): Размер файла в байтах.
    """
    filename: str
    size: int


class FileInfoShort(_BaseFileInfo):
    """Краткая информация о файле.
    
    Params:
        filename (str): Имя файла.
        size (int): Размер файла в байтах.
    """
    pass


class FileInfoVerbose(_BaseFileInfo):
    """Подробная информация о файле.
    
    Params:
        filename (str): Имя файла.
        size (int): Размер файла в байтах.
        content_type (str | None): MIME-тип содержимого файла.
        atime (float): Время последнего доступа к файлу в формате timestamp -
            секунды с начала эпохи.
        mtime (float): Время последнего изменения файла в формате timestamp -
            секунды с начала эпохи.
    """
    content_type: str | None
    atime: float
    mtime: float


class StorageUsageInfo(BaseModel):
    """Информация об использовании места хранилища.
    
    Params:
        used (int): Использованное пространство хранилища в байтах.
        free (int): Свободное пространство хранилища в байтах.
    """
    used: int
    free: int
