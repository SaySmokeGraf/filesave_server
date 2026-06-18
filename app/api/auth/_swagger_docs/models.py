"""Документация для моделей."""

from app.api.utils.swagger_docs.models import (
    ModelDocsParams, ModelJSONSchemaParams
)


_TOKEN_DESC = """
Модель токена.

Содержит в себе непосредственно токен и его тип.
"""
token = ModelDocsParams(
    title='Token: Токен',
    json_schema_extra=ModelJSONSchemaParams(
        description=_TOKEN_DESC,
        examples=[
            {'access_token': 'someAC.CESStoken.JWT', 'token_type': 'bearer'}
        ]
    ).docs_dump()
)
