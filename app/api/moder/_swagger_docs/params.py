"""Документация для параметров."""

from app.api.utils.swagger_docs.models import FieldDocsParams


_UPDATE_RIGHTS_DESC = """
Модель обновления прав доступа пользователя.

Схема: UserUpdateRights.
"""
update_rights = FieldDocsParams(
    title='Обновление прав пользователя',
    description=_UPDATE_RIGHTS_DESC
)

username = FieldDocsParams(
    title='Имя пользователя',
    description='Имя пользователя.'
)
