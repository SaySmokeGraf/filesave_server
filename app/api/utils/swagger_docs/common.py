"""Общие для приложения экземпляры моделей документации.

Consts:
    RESP_XXX_SIMPLE_MSG_CONTENT (JSONLikeDict): Контент схема для ответа с
        простым сообщением в параметре detail.

Contains:
    header_www_auth (HeaderDocsParams): Документация на заголовок
        WWW-Authenticate.
    resp_200_simple_msg (ResponseDocsParams): Ответ 200 с простым сообщением.
    resp_401_token (ResponseDocsParams): Ответ 401 при невалидном токене.
    resp_403_moder (ResponseDocsParams): Ответ 403 при отсутствии прав для
        модерирования (в т.ч. и более базовых пользовательских).
    resp_403_no_permission (ResponseDocsParams): Ответ 403 при отсутствии прав
        на действие (модерирование + защита от правок модером модеров).
    resp_403_user (ResponseDocsParams): Ответ 403 при отсутствии прав на
        базовые действия пользователя.
    resp_404_file (ResponseDocsParams): Ответ 404 - файл не найден.
    resp_404_user (ResponseDocsParams): Ответ 404 - пользователь не найден.
    resp_409_no_permission (ResponseDocsParams): Ответ 409 - нет доступа к
        действию по причине занятости ресурса.
    resp_422_validation (ResponseDocsParams): Ответ 422 - общая ошибка
        валидации входных данных.
"""

from app.api.utils.swagger_docs.models import (
    ResponseDocsParams, HeaderDocsParams
)


# вспомогательные константы
_RESP_XXX_SIMPLE_MSG_EXAMPLE = {'detail': 'string'}
_RESP_422_STD_EXAMPLE = {
    'detail': [
        {
            'loc': ['string', 0],
            'msg': 'string',
            'type': 'string',
            'input': 'string',
            'ctx': {}
        }
    ]
}

RESP_XXX_SIMPLE_MSG_CONTENT = {
    'application/json': {'example': _RESP_XXX_SIMPLE_MSG_EXAMPLE}
}
_RESP_422_STD_CONTENT = {
    'application/json': {'example': _RESP_422_STD_EXAMPLE}
}


# вспомогательные заголовки
_HEADER_WWW_AUTH_DESC = """
Стандартный заголовок, требуемый согласно спецификации.

В контексте данного сервиса всегда имеет значение 'Bearer'.
"""
header_www_auth = HeaderDocsParams(
    description=_HEADER_WWW_AUTH_DESC,
    schema_={'type': 'string', 'example': 'Bearer'},
    required=True
)


# ответы 2хх
resp_200_simple_msg = ResponseDocsParams(
    description='Успешное выполнение с сообщением в detail.',
    content=RESP_XXX_SIMPLE_MSG_CONTENT
)


# ответы 4хх
_RESP_401_TOKEN_DESC = """
Пользователь не аутентифицирован.

Причина: невалидный токен.
"""
resp_401_token = ResponseDocsParams(
    description=_RESP_401_TOKEN_DESC,
    headers={'WWW-Authenticate': header_www_auth.docs_dump()},
    content=RESP_XXX_SIMPLE_MSG_CONTENT
)

_RESP_403_USER_DESC = """
Недостаточно прав на действие.

Возможные причины: токен относится к пользователю, который забанен или
неверифицирован.
"""
resp_403_user = ResponseDocsParams(
    description=_RESP_403_USER_DESC,
    content=RESP_XXX_SIMPLE_MSG_CONTENT
)

_RESP_403_MODER_DESC = """
Недостаточно прав на действие.

Возможные причины: токен относится к пользователю, который не является
модератором, забанен или неверифицирован.
"""
resp_403_moder = ResponseDocsParams(
    description=_RESP_403_MODER_DESC,
    content=RESP_XXX_SIMPLE_MSG_CONTENT
)

_RESP_403_NO_PERMISSION = """
Недостаточно прав на действие.

Возможные причины: токен относится к пользователю, который не является
модератором, забанен или неверифицирован; модератор пытается удалить или
обновить права другого модератора.
"""
resp_403_no_permission = ResponseDocsParams(
    description=_RESP_403_NO_PERMISSION,
    content=RESP_XXX_SIMPLE_MSG_CONTENT
)

resp_404_user = ResponseDocsParams(
    description='Пользователь с такими параметрами не найден.',
    content=RESP_XXX_SIMPLE_MSG_CONTENT
)

resp_404_file = ResponseDocsParams(
    description='Файл с такими параметрами не найден.',
    content=RESP_XXX_SIMPLE_MSG_CONTENT
)

_RESP_409_NO_PERMISSION_DESC = """
Нет доступа для удаления.

Возможные причины: файл или папка пользователя занята сервером и не может быть
удалена в текущий момент.
"""
resp_409_no_permission = ResponseDocsParams(
    description=_RESP_409_NO_PERMISSION_DESC,
    content=RESP_XXX_SIMPLE_MSG_CONTENT
)

resp_422_validation = ResponseDocsParams(
    description='Ошибка валидации входных данных.',
    content=_RESP_422_STD_CONTENT
)
