"""Документация для параметров."""

from app.api.utils.swagger_docs.models import FieldDocsParams


filename = FieldDocsParams(
    title='Имя файла',
    description='Имя файла в формате <стэм>.<расширение>.'
)

_OVERWRITE_DESC = """
Флаг перезаписи файла в случае наличия файла с таким же именем в хранилище.

Значения: true - перезаписать, false - создать уникальное имя с помощью
суффикса с номером, null (отсутствие инструкций) - откинуть ошибку.

По умолчанию null.
"""
overwrite = FieldDocsParams(
    title='Флаг перезаписи файла',
    description=_OVERWRITE_DESC
)

_RENAME_DESC = """
Флаг переименования файла в случае небезопасного имени.

При значении false вызывает ошибку в случае небезопасного имени. При true -
автоматически переименовывает на безопасное имя по необходимости.

По умолчанию false.
"""
rename = FieldDocsParams(
    title='Флаг переименования файла',
    description=_RENAME_DESC
)
