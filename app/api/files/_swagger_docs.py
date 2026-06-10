"""Документация для отображения в OpenAPI (Swagger) для пакета files."""

from fastapi import status

import app.api.utils.swagger_docs.common as swcommon
from app.api.utils.swagger_docs.models import (
    EndpointDocsParams, HeaderDocsParams, ResponseDocsParams, RouterDocsParams
)


# заголовки
_HEADER_CONTENT_DISPOSITION_DESC = """
Заголовок, отвечающий за расположение контента в ответе.

В данном случае всегда принимает значение 'attachment' для передачи в
прикрепленном к ответу виде для скачивания файла, а не его открытия в браузере.
"""
_header_content_disposition = HeaderDocsParams(
    description=_HEADER_CONTENT_DISPOSITION_DESC,
    schema_={'type': 'string', 'example': 'attachment'},
    required=True
)


# ответы
_RESP_200_FILES_LIST_DESC = """
Список данных о файле в кратком формате.

Схема: FileInfoShort.
"""
_resp_200_files_list = ResponseDocsParams(
    description=_RESP_200_FILES_LIST_DESC
)

_RESP_200_FILE_INFO_DESC = """
Подробная информация о файле.

Схема: FileInfoVerbose.
"""
_resp_200_file_info = ResponseDocsParams(
    description=_RESP_200_FILE_INFO_DESC
)

_RESP_200_STORAGE_INFO_DESC = """
Информация об использовании хранилища.

Схема: StorageUsageInfo.
"""
_resp_200_storage_info = ResponseDocsParams(
    description=_RESP_200_STORAGE_INFO_DESC
)

_RESP_200_FILE_DESC = """
Успешная обработка и начало отправки файла.

К ответу в прикрепленном (attachment) формате прилагается файл для скачивания.
"""
_resp_200_file = ResponseDocsParams(
    description=_RESP_200_FILE_DESC,
    headers={'Content-Disposition': _header_content_disposition.docs_dump()},
    content=None
)

_resp_201_uploaded = ResponseDocsParams(
    description='Файл загружен успешно.',
    content=swcommon.RESP_XXX_SIMPLE_MSG_CONTENT
)

_RESP_400_UNSAFE_DESC = """
Небезопасное имя файла.

Имя файла небезопасно, при этом флаг rename равен False (указывает на отказ от
переименования).
"""
_resp_400_unsafe = ResponseDocsParams(
    description=_RESP_400_UNSAFE_DESC,
    content=swcommon.RESP_XXX_SIMPLE_MSG_CONTENT
)

_RESP_409_OVERWRITE_DESC = """
Коллизия имен.

Файл с таким именем есть в хранилище, но нет указаний на этот случай во флаге
overwrite.
"""
_resp_409_overwrite = ResponseDocsParams(
    description=_RESP_409_OVERWRITE_DESC,
    content=swcommon.RESP_XXX_SIMPLE_MSG_CONTENT
)

_resp_413_too_large = ResponseDocsParams(
    description='Размер файла слишком велик.',
    content=swcommon.RESP_XXX_SIMPLE_MSG_CONTENT
)


# роутеры
router = RouterDocsParams(
    tags=['files'],
    responses={
        401: swcommon.resp_401_token.docs_dump(),
        403: swcommon.resp_403_user.docs_dump(),
        422: swcommon.resp_422_validation.docs_dump()
    }
)


# эндпоинты
_GET_FILES_DATA_DESC = """
Получить список с данными о файлах пользователя.

Требуется авторизационный заголовок с токеном типа Bearer верифицированного
незабаненного пользователя.
"""
get_files_data = EndpointDocsParams(
    status_code=status.HTTP_200_OK,
    summary='Получить список файлов',
    description=_GET_FILES_DATA_DESC,
    responses={
        200: _resp_200_files_list.docs_dump()
    }
)

_GET_FILE_INFO_DESC = """
Получить подробную информацию о файле по его имени.

Требуется авторизационный заголовок с токеном типа Bearer верифицированного
незабаненного пользователя.
"""
get_file_info = EndpointDocsParams(
    status_code=status.HTTP_200_OK,
    summary='Получить подробную информацию о файле',
    description=_GET_FILE_INFO_DESC,
    responses={
        200: _resp_200_file_info.docs_dump(),
        404: swcommon.resp_404_file.docs_dump()
    }
)

_GET_STORAGE_INFO_DESC = """
Получить информацию об использовании хранилища.

Требуется авторизационный заголовок с токеном типа Bearer верифицированного
незабаненного пользователя.
"""
get_storage_info = EndpointDocsParams(
    status_code=status.HTTP_200_OK,
    summary='Получить информацию о хранилище',
    description=_GET_STORAGE_INFO_DESC,
    responses={
        200: _resp_200_storage_info.docs_dump()
    }
)

_DOWNLOAD_FILE_DESC = """
Скачать файл с сервера по его имени.

Требуется авторизационный заголовок с токеном типа Bearer верифицированного
незабаненного пользователя.
"""
download_file = EndpointDocsParams(
    status_code=status.HTTP_200_OK,
    summary='Скачать файл с сервера',
    description=_DOWNLOAD_FILE_DESC,
    responses={
        200: _resp_200_file.docs_dump(),
        404: swcommon.resp_404_file.docs_dump()
    }
)

_UPLOAD_SINGLE_FILE_DESC = """
Загрузить один файл на сервер.

Принимает в себя файл в виде данных формы и необязательные параметры на случай
конфликтных ситуаций.

Требуется авторизационный заголовок с токеном типа Bearer верифицированного
незабаненного пользователя.
"""
upload_single_file = EndpointDocsParams(
    status_code=status.HTTP_201_CREATED,
    summary='Загрузить файл на сервер',
    description=_UPLOAD_SINGLE_FILE_DESC,
    responses={
        201: _resp_201_uploaded.docs_dump(),
        400: _resp_400_unsafe.docs_dump(),
        409: _resp_409_overwrite.docs_dump(),
        413: _resp_413_too_large.docs_dump()
    }
)

_DELETE_FILE_DESC = """
Удалить файл с сервера по имени файла.

Требуется авторизационный заголовок с токеном типа Bearer верифицированного
незабаненного пользователя.
"""
delete_file = EndpointDocsParams(
    status_code=status.HTTP_200_OK,
    summary='Удалить файл с сервера',
    description=_DELETE_FILE_DESC,
    responses={
        200: swcommon.resp_200_simple_msg.docs_dump(),
        404: swcommon.resp_404_file.docs_dump(),
        409: swcommon.resp_409_no_permission.docs_dump()
    }
)
