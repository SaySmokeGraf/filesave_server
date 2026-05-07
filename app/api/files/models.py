"""Модели для файлового API."""

from pydantic import BaseModel


class _BaseFileInfo(BaseModel):
    """Базовая модель информации о файле."""
    filename: str
    size: int


class FileInfoShort(_BaseFileInfo):
    """Краткая информация о файле."""
    pass


class FileInfoVerbose(_BaseFileInfo):
    """Подробная информация о файле."""
    content_type: str | None
    atime: float
    mtime: float


class StorageUsageInfo(BaseModel):
    """Информация об использовании места хранилища."""
    used: int
    free: int
