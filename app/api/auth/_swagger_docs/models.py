"""Документация для моделей."""

import app.api.auth._swagger_docs._json_schemas as _json_schemas
from app.api.utils.swagger_docs.models import ModelDocsParams


token = ModelDocsParams(
    title='Token: Токен',
    json_schema_extra=_json_schemas.token.docs_dump()
)
