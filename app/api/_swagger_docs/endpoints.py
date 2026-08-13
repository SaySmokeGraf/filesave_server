"""Документация для эндпоинтов."""

from fastapi import status

from app.api.utils.swagger_docs.models import EndpointDocsParams


get_root = EndpointDocsParams(
    status_code=status.HTTP_308_PERMANENT_REDIRECT,
    tags=['common'],
    summary='Корень',
    description='Корневой эндпоинт сервиса. Перенаправляет на статические файлы фронтенда.',
    response_description='Перенаправление на эндпоинт фронтенда.'
)
