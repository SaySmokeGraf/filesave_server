"""Документация для ответов."""

import app.api.utils.swagger_docs.common as swcommon
from app.api.utils.swagger_docs.models import ResponseDocsParams


# вспомогательные константы
_RESP_2XX_TOKEN_DESC = """
Успешное выполнение с возвратом токена.

Схема: Token.
"""


# основные ответы
s200_token = ResponseDocsParams(
    description=_RESP_2XX_TOKEN_DESC
)

_S200_USER_INFO_DESC = """
Публичная информация о пользователе.

Схема: UserPublic.
"""
s200_user_info = ResponseDocsParams(
    description=_S200_USER_INFO_DESC
)

s201_token = ResponseDocsParams(
    description=_RESP_2XX_TOKEN_DESC
)

_S401_AUTH_DATA_DESC = """
Пользователь не аутентифицирован.

Причина: невалидные данные для аутентификации.
"""
s401_auth_data = ResponseDocsParams(
    description=_S401_AUTH_DATA_DESC,
    headers={
        'WWW-Authenticate': swcommon.header_www_auth.docs_dump()
    },
    content=swcommon.RESP_XXX_SIMPLE_MSG_CONTENT
)

_S403_REG_DATA_DESC = """
Пользователь не зарегистрирован.

Причина: пользователь с таким именем уже существует.
"""
s403_reg_data = ResponseDocsParams(
    description=_S403_REG_DATA_DESC,
    headers={
        'WWW-Authenticate': swcommon.header_www_auth.docs_dump()
    },
    content=swcommon.RESP_XXX_SIMPLE_MSG_CONTENT
)

s422_reg_form = ResponseDocsParams(
    description='Невалидные данные в форме регистрации',
    headers={
        'WWW-Authenticate': swcommon.header_www_auth.docs_dump()
    },
    content=swcommon.RESP_XXX_SIMPLE_MSG_CONTENT
)
