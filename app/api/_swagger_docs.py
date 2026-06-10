"""Документация для отображения в OpenAPI (Swagger) для пакета api."""

from fastapi import status

from app.api.utils.swagger_docs.models import EndpointDocsParams


# эндпоинты
get_root = EndpointDocsParams(
    status_code=status.HTTP_308_PERMANENT_REDIRECT,
    tags=['common'],
    summary='Корень',
    description='Корневой эндпоинт сервиса. Перенаправляет на статические файлы фронтенда.',
    response_description='Перенаправление на эндпоинт фронтенда.'
)
