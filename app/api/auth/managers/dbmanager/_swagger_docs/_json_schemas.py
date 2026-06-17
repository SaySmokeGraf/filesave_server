"""JSON-схемы для документации моделей."""

from app.api.utils.swagger_docs.models import ModelJSONSchemaParams


user_public = ModelJSONSchemaParams(
    description='Публичная информация о пользователе.',
    examples=[
        {'id': 0, 'username': 'arbuz', 'is_verified': True,
         'is_moderator': True, 'is_banned': False}
    ]
)

_USER_UPDATERIGHTS_DESC = """
Модель обновления прав доступа пользователя.

Все параметры подразумевают, что неуказание какого-либо параметра равно
оставить право доступа без изменений. В ином случае устанавливается указанное
значение.
"""
user_updaterights = ModelJSONSchemaParams(
    description=_USER_UPDATERIGHTS_DESC,
    examples=[
        {'is_verified': True, 'is_moderator': True, 'is_banned': False},
        {'is_banned': True},
        {'is_verified': True},
        {'is_moderator': False, 'is_banned': True}
    ]
)

paged_users_public = ModelJSONSchemaParams(
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
)
