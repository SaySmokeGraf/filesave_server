"""JSON-схемы для документирования моделей."""

from app.api.utils.swagger_docs.models import ModelJSONSchemaParams


_TOKEN_DESC = """
Модель токена.

Содержит в себе непосредственно токен и его тип.
"""
token = ModelJSONSchemaParams(
    description=_TOKEN_DESC,
    examples=[
        {'access_token': 'someAC.CESStoken.JWT', 'token_type': 'bearer'}
    ]
)
