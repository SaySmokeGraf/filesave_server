"""Модели для файлового API.

Models:
    FileInfoShort: Краткая информация о файле.
    FileInfoVerbose: Подробная информация о файле.
    StorageUsageInfo: Информация об использовании места хранилища.
"""

from pydantic import BaseModel, Field

import app.api.files._swagger_docs as swdocs


class _BaseFileInfo(BaseModel):
    """Базовая модель информации о файле.

    Params:
        filename (str): Имя файла.
        size (int): Размер файла в байтах.
    """
    filename: str = Field(**swdocs.fields.filename.docs_dump())
    size: int = Field(**swdocs.fields.size.docs_dump())


class FileInfoShort(_BaseFileInfo):
    """Краткая информация о файле.
    
    Params:
        filename (str): Имя файла.
        size (int): Размер файла в байтах.
    """
    model_config = swdocs.models.short_info.docs_dump()


class FileInfoVerbose(_BaseFileInfo):
    """Подробная информация о файле.
    
    Params:
        filename (str): Имя файла.
        size (int): Размер файла в байтах.
        content_type (str | None): MIME-тип содержимого файла.
        atime (float): Время последнего доступа к файлу в формате Epoch Unix
            Timestamp - секунды с начала эпохи.
        mtime (float): Время последнего изменения файла в формате Epoch Unix
            Timestamp - секунды с начала эпохи.
    """
    model_config = swdocs.models.verbose_info.docs_dump()

    content_type: str | None = Field(**swdocs.fields.content_type.docs_dump())
    atime: float = Field(**swdocs.fields.atime.docs_dump())
    mtime: float = Field(**swdocs.fields.mtime.docs_dump())


class StorageUsageInfo(BaseModel):
    """Информация об использовании места хранилища.
    
    Params:
        used (int): Использованное пространство хранилища в байтах.
        free (int): Свободное пространство хранилища в байтах.
    """
    model_config = swdocs.models.storage.docs_dump()
    
    used: int = Field(**swdocs.fields.used.docs_dump())
    free: int = Field(**swdocs.fields.free.docs_dump())
