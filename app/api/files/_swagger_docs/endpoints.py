"""Документация для эндпоинтов."""

from fastapi import status

import app.api.files._swagger_docs._responses as _resps
import app.api.utils.swagger_docs.common as swcommon
from app.api.utils.swagger_docs.models import EndpointDocsParams


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
        200: _resps.s200_files_list.docs_dump()
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
        200: _resps.s200_file_info.docs_dump(),
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
        200: _resps.s200_storage_info.docs_dump()
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
        200: _resps.s200_file.docs_dump(),
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
        201: _resps.s201_uploaded.docs_dump(),
        400: _resps.s400_unsafe.docs_dump(),
        409: _resps.s409_overwrite.docs_dump(),
        413: _resps.s413_too_large.docs_dump()
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
