"""Документация для отображения в OpenAPI (Swagger) для пакета dbmanager."""

from app.api.utils.swagger_docs.models import (
    ModelDocsParams, ModelJSONSchemaParams, FieldDocsParams
)


# JSON-схемы моделей
_json_schema_user_public = ModelJSONSchemaParams(
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
_json_schema_user_updaterights = ModelJSONSchemaParams(
    description=_USER_UPDATERIGHTS_DESC,
    examples=[
        {'is_verified': True, 'is_moderator': True, 'is_banned': False},
        {'is_banned': True},
        {'is_verified': True},
        {'is_moderator': False, 'is_banned': True}
    ]
)

_json_schema_paged_users_public = ModelJSONSchemaParams(
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


# модели
model_user_public = ModelDocsParams(
    title='UserPublic: Публичная модель пользователя',
    json_schema_extra=_json_schema_user_public.docs_dump()
)

model_user_updaterights = ModelDocsParams(
    title='UserUpdateRights: Обновление прав пользователя',
    json_schema_extra=_json_schema_user_updaterights.docs_dump()
)

model_paged_users_public = ModelDocsParams(
    title='PagedUsersPublic: Пагинированный список публичных пользователей',
    json_schema_extra=_json_schema_paged_users_public.docs_dump()
)


# поля
field_username = FieldDocsParams(
    title='Имя пользователя',
    description='Имя пользователя.'
)

field_id = FieldDocsParams(
    title='ID',
    description='ID пользователя в БД.'
)

field_is_verified = FieldDocsParams(
    title='Верифицированность',
    description='Флаг верифицированности пользователя.'
)

field_is_moderator = FieldDocsParams(
    title='Право модерировать',
    description='Флаг наличия прав модератора у пользователя.'
)

field_is_banned = FieldDocsParams(
    title='Забаненность',
    description='Флаг забаненности пользователя.'
)

field_items_users = FieldDocsParams(
    title='Список пользователей',
    description='Список пользователей на этой странице.',
    examples=[
        [
            {'id': 0, 'username': 'arbuz', 'is_verified': True,
            'is_moderator': True, 'is_banned': False},
            {'id': 1, 'username': 'kavun', 'is_verified': True,
            'is_moderator': False, 'is_banned': True},
            {'id': 2, 'username': 'watermelon', 'is_verified': False,
            'is_moderator': False, 'is_banned': False}
        ]
    ]
)

field_total_users = FieldDocsParams(
    title='Всего пользователей',
    description='Общее число пользователей по этому запросу.'
)

field_page_users = FieldDocsParams(
    title='Номер страницы',
    description='Номер страницы.'
)

field_limit_users = FieldDocsParams(
    title='Пользователей на странице',
    description='Число пользователей на одной странице.'
)

field_username_filter = FieldDocsParams(
    title='Фильтр по имени пользователя',
    description='Фильтр по подстроке в имени пользователя без учета регистра.'
)
