"""Документация для эндпоинтов."""

from fastapi import status

import app.api.auth._swagger_docs._responses as _resps
import app.api.utils.swagger_docs.common as swcommon
from app.api.utils.swagger_docs.models import EndpointDocsParams


_LOGIN_DESC = """
Войти на сервис за существующего пользователя.

В случае успешного выполнения возвращает токен.
"""
login = EndpointDocsParams(
    status_code=status.HTTP_200_OK,
    summary='Вход на сервис',
    description=_LOGIN_DESC,
    responses={
        200: _resps.s200_token.docs_dump(),
        401: _resps.s401_auth_data.docs_dump()
    }
)

_REGISTER_DESC = """
Зарегистрировать нового пользователя.

В случае успешного выполнения возвращает токен.

Важно: зарегистрированный пользователь по умолчанию не верифицирован и не будет
иметь достаточных прав доступа для использования сервиса до тех пор, пока не
будет подтвержден модератором.
"""
register = EndpointDocsParams(
    status_code=status.HTTP_201_CREATED,
    summary='Регистрация',
    description=_REGISTER_DESC,
    responses={
        201: _resps.s201_token.docs_dump(),
        403: _resps.s403_reg_data.docs_dump(),
        422: _resps.s422_reg_form.docs_dump()
    }
)

_GET_USER_INFO_DESC = """
Получить публичную информацию о пользователе по его токену.

Требуется валидный токен в соответствующем заголовке.
"""
get_user_info = EndpointDocsParams(
    status_code=status.HTTP_200_OK,
    summary='Информация о пользователе',
    description=_GET_USER_INFO_DESC,
    responses={
        200: _resps.s200_user_info.docs_dump(),
        401: swcommon.resp_401_token.docs_dump()
    }
)
