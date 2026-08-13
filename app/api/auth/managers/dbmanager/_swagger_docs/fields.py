"""Документация для полей."""

from app.api.utils.swagger_docs.models import FieldDocsParams


username = FieldDocsParams(
    title='Имя пользователя',
    description='Имя пользователя.'
)

id = FieldDocsParams(
    title='ID',
    description='ID пользователя в БД.'
)

is_verified = FieldDocsParams(
    title='Верифицированность',
    description='Флаг верифицированности пользователя.'
)

is_moderator = FieldDocsParams(
    title='Право модерировать',
    description='Флаг наличия прав модератора у пользователя.'
)

is_banned = FieldDocsParams(
    title='Забаненность',
    description='Флаг забаненности пользователя.'
)

items_users = FieldDocsParams(
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

total_users = FieldDocsParams(
    title='Всего пользователей',
    description='Общее число пользователей по этому запросу.'
)

page_users = FieldDocsParams(
    title='Номер страницы',
    description='Номер страницы.'
)

limit_users = FieldDocsParams(
    title='Пользователей на странице',
    description='Число пользователей на одной странице.'
)

username_filter = FieldDocsParams(
    title='Фильтр по имени пользователя',
    description='Фильтр по подстроке в имени пользователя без учета регистра.'
)
