"""Документация для моделей."""

from app.api.utils.swagger_docs.models import (
    ModelDocsParams, ModelJSONSchemaParams
)


user_public = ModelDocsParams(
    title='UserPublic: Публичная модель пользователя',
    json_schema_extra=ModelJSONSchemaParams(
        description='Публичная информация о пользователе.',
        examples=[
            {'id': 0, 'username': 'arbuz', 'is_verified': True,
             'is_moderator': True, 'is_banned': False}
        ]
    ).docs_dump()
)

_USER_UPDATERIGHTS_DESC = """
Модель обновления прав доступа пользователя.

Все параметры подразумевают, что неуказание какого-либо параметра равно
оставить право доступа без изменений. В ином случае устанавливается указанное
значение.
"""
user_updaterights = ModelDocsParams(
    title='UserUpdateRights: Обновление прав пользователя',
    json_schema_extra=ModelJSONSchemaParams(
        description=_USER_UPDATERIGHTS_DESC,
        examples=[
            {'is_verified': True, 'is_moderator': True, 'is_banned': False},
            {'is_banned': True},
            {'is_verified': True},
            {'is_moderator': False, 'is_banned': True}
        ]
    ).docs_dump()
)

paged_users_public = ModelDocsParams(
    title='PagedUsersPublic: Пагинированный список публичных пользователей',
    json_schema_extra=ModelJSONSchemaParams(
        description='Пагинированный список публичных пользователей.',
        examples=[
            {
                'items': [
                    {'id': 0, 'username': 'arbuz', 'is_verified': True,
                     'is_moderator': True, 'is_banned': False},
                    {'id': 1, 'username': 'kavun', 'is_verified': True,
                     'is_moderator': False, 'is_banned': True},
                    {'id': 2, 'username': 'watermelon', 'is_verified': False,
                     'is_moderator': False, 'is_banned': False}
                ],
                'total': 100, 'page': 1, 'limit': 3
            }
        ]
    ).docs_dump()
)
