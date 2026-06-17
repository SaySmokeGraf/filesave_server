"""Документация для отображения в OpenAPI (Swagger) для пакета moder."""

from fastapi import status

import app.api.utils.swagger_docs.common as swcommon
from app.api.utils.swagger_docs.models import (
    FieldDocsParams,
    EndpointDocsParams, ResponseDocsParams, RouterDocsParams
)


# параметры
query_username = FieldDocsParams(
    title='Имя пользователя',
    description='Имя пользователя.'
)

_BODY_UPDATE_RIGHTS_DESC = """
Модель обновления прав доступа пользователя.

Схема: UserUpdateRights.
"""
body_update_rights = FieldDocsParams(
    title='Обновление прав пользователя',
    description=_BODY_UPDATE_RIGHTS_DESC
)


# ответы
_RESP_200_PAGE_DESC = """
Страница из списка пользователей.

Схема: PagedUsersPublic.
"""
_resp_200_page = ResponseDocsParams(
    description=_RESP_200_PAGE_DESC
)


# роутеры
router = RouterDocsParams(
    tags=['moderation'],
    responses={
        401: swcommon.resp_401_token.docs_dump(),
        422: swcommon.resp_422_validation.docs_dump()
    }
)


# эндпоинты
_GET_USERS_DESC = """
Получить страницу из списка пользователей.

Обязательная пагинация и необязательные параметры фильтрации. Требуется
авторизационный заголовок с токеном типа Bearer пользователя с правами
модератора.
"""
get_users = EndpointDocsParams(
    status_code=status.HTTP_200_OK,
    summary='Получить список пользователей',
    description=_GET_USERS_DESC,
    responses={
        200: _resp_200_page.docs_dump(),
        403: swcommon.resp_403_moder.docs_dump()
    }
)

_DELETE_USER_DESC = """
Удалить пользователя по его имени пользователя.

Требуется авторизационный заголовок с токеном типа Bearer пользователя с
правами модератора.
"""
delete_user = EndpointDocsParams(
    status_code=status.HTTP_200_OK,
    summary='Удалить пользователя',
    description=_DELETE_USER_DESC,
    responses={
        200: swcommon.resp_200_simple_msg.docs_dump(),
        403: swcommon.resp_403_no_permission.docs_dump(),
        404: swcommon.resp_404_user.docs_dump(),
        409: swcommon.resp_409_no_permission.docs_dump()
    }
)

_UPDATE_USER_RIGHTS_DESC = """
Обновить права доступа пользователя по имени пользователя и данным для
обновления.

Требуется авторизационный заголовок с токеном типа Bearer пользователя с
правами модератора.
"""
update_user_rights = EndpointDocsParams(
    status_code=status.HTTP_200_OK,
    summary='Обновить права доступа пользователя',
    description=_UPDATE_USER_RIGHTS_DESC,
    responses={
        200: swcommon.resp_200_simple_msg.docs_dump(),
        403: swcommon.resp_403_no_permission.docs_dump(),
        404: swcommon.resp_404_user.docs_dump()
    }
)
