"""Документация для отображения в OpenAPI (Swagger) для пакета auth."""

from fastapi import status

import app.api.utils.swagger_docs.common as swcommon
from app.api.utils.swagger_docs.models import (
    ModelDocsParams, ModelJSONSchemaParams, FieldDocsParams,
    EndpointDocsParams, ResponseDocsParams, RouterDocsParams
)


# вспомогательные константы
_RESP_2XX_TOKEN_DESC = """
Успешное выполнение с возвратом токена.

Схема: Token.
"""


# JSON-схемы моделей
_TOKEN_DESC = """
Модель токена.

Содержит в себе непосредственно токен и его тип.
"""
_json_schema_token = ModelJSONSchemaParams(
    description=_TOKEN_DESC,
    examples=[
        {'access_token': 'someAC.CESStoken.JWT', 'token_type': 'bearer'}
    ]
)


# модели
model_token = ModelDocsParams(
    title='Token: Токен',
    json_schema_extra=_json_schema_token.docs_dump()
)


# поля
field_access_token = FieldDocsParams(
    title='Токен',
    description='Токен.',
    examples=['someAC.CESStoken.JWT', 's0meotH3r.ACC3ssT0K3N.B3Ar3rJWT']
)

field_token_type = FieldDocsParams(
    title='Тип токена',
    description='Тип токена.',
    examples=['bearer']
)


# ответы
_resp_200_token = ResponseDocsParams(
    description=_RESP_2XX_TOKEN_DESC
)

_RESP_200_USER_INFO_DESC = """
Публичная информация о пользователе.

Схема: UserPublic.
"""
_resp_200_user_info = ResponseDocsParams(
    description=_RESP_200_USER_INFO_DESC
)

_resp_201_token = ResponseDocsParams(
    description=_RESP_2XX_TOKEN_DESC
)

_RESP_401_AUTH_DATA_DESC = """
Пользователь не аутентифицирован.

Причина: невалидные данные для аутентификации.
"""
_resp_401_auth_data = ResponseDocsParams(
    description=_RESP_401_AUTH_DATA_DESC,
    headers={
        'WWW-Authenticate': swcommon.header_www_auth.docs_dump()
    },
    content=swcommon.RESP_XXX_SIMPLE_MSG_CONTENT
)

_RESP_403_REG_DATA_DESC = """
Пользователь не зарегистрирован.

Причина: пользователь с таким именем уже существует.
"""
_resp_403_reg_data = ResponseDocsParams(
    description=_RESP_403_REG_DATA_DESC,
    headers={
        'WWW-Authenticate': swcommon.header_www_auth.docs_dump()
    },
    content=swcommon.RESP_XXX_SIMPLE_MSG_CONTENT
)

_resp_422_reg_form = ResponseDocsParams(
    description='Невалидные данные в форме регистрации',
    headers={
        'WWW-Authenticate': swcommon.header_www_auth.docs_dump()
    },
    content=swcommon.RESP_XXX_SIMPLE_MSG_CONTENT
)


# роутер
router = RouterDocsParams(
    tags=['authorization'],
    responses={
        422: swcommon.resp_422_validation.docs_dump(),
    }
)


# эндпоинты
_LOGIN_DESC = """
Войти на сервис за существующего пользователя.

В случае успешного выполнения возвращает токен.
"""
login = EndpointDocsParams(
    status_code=status.HTTP_200_OK,
    summary='Вход на сервис',
    description=_LOGIN_DESC,
    responses={
        200: _resp_200_token.docs_dump(),
        401: _resp_401_auth_data.docs_dump()
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
        201: _resp_201_token.docs_dump(),
        403: _resp_403_reg_data.docs_dump(),
        422: _resp_422_reg_form.docs_dump()
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
        200: _resp_200_user_info.docs_dump(),
        401: swcommon.resp_401_token.docs_dump()
    }
)
