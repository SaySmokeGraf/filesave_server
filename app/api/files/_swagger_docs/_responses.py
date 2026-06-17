"""Документация для ответов."""

import app.api.files._swagger_docs._headers as _headers
import app.api.utils.swagger_docs.common as swcommon
from app.api.utils.swagger_docs.models import ResponseDocsParams


_S200_FILES_LIST_DESC = """
Список данных о файле в кратком формате.

Схема: FileInfoShort.
"""
s200_files_list = ResponseDocsParams(
    description=_S200_FILES_LIST_DESC
)

_S200_FILE_INFO_DESC = """
Подробная информация о файле.

Схема: FileInfoVerbose.
"""
s200_file_info = ResponseDocsParams(
    description=_S200_FILE_INFO_DESC
)

_S200_STORAGE_INFO_DESC = """
Информация об использовании хранилища.

Схема: StorageUsageInfo.
"""
s200_storage_info = ResponseDocsParams(
    description=_S200_STORAGE_INFO_DESC
)

_S200_FILE_DESC = """
Успешная обработка и начало отправки файла.

К ответу в прикрепленном (attachment) формате прилагается файл для скачивания.
"""
s200_file = ResponseDocsParams(
    description=_S200_FILE_DESC,
    headers={'Content-Disposition': _headers.content_disposition.docs_dump()},
    content=None
)

s201_uploaded = ResponseDocsParams(
    description='Файл загружен успешно.',
    content=swcommon.RESP_XXX_SIMPLE_MSG_CONTENT
)

_S400_UNSAFE_DESC = """
Небезопасное имя файла.

Имя файла небезопасно, при этом флаг rename равен False (указывает на отказ от
переименования).
"""
s400_unsafe = ResponseDocsParams(
    description=_S400_UNSAFE_DESC,
    content=swcommon.RESP_XXX_SIMPLE_MSG_CONTENT
)

_S409_OVERWRITE_DESC = """
Коллизия имен.

Файл с таким именем есть в хранилище, но нет указаний на этот случай во флаге
overwrite.
"""
s409_overwrite = ResponseDocsParams(
    description=_S409_OVERWRITE_DESC,
    content=swcommon.RESP_XXX_SIMPLE_MSG_CONTENT
)

s413_too_large = ResponseDocsParams(
    description='Размер файла слишком велик.',
    content=swcommon.RESP_XXX_SIMPLE_MSG_CONTENT
)
