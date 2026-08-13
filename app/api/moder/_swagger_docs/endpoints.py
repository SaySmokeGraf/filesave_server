"""Документация для эндпоинтов."""

from fastapi import status

import app.api.moder._swagger_docs._responses as _resps
import app.api.utils.swagger_docs.common as swcommon
from app.api.utils.swagger_docs.models import EndpointDocsParams


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
        200: _resps.s200_page.docs_dump(),
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
update_user = EndpointDocsParams(
    status_code=status.HTTP_200_OK,
    summary='Обновить права доступа пользователя',
    description=_UPDATE_USER_RIGHTS_DESC,
    responses={
        200: swcommon.resp_200_simple_msg.docs_dump(),
        403: swcommon.resp_403_no_permission.docs_dump(),
        404: swcommon.resp_404_user.docs_dump()
    }
)
