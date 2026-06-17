"""Документация для моделей."""

import app.api.files._swagger_docs._json_schemas as _json_schemas
from app.api.utils.swagger_docs.models import ModelDocsParams


short_info = ModelDocsParams(
    title='FileInfoShort: Краткая информация о файле',
    json_schema_extra=_json_schemas.short_info.docs_dump()
)

verbose_info = ModelDocsParams(
    title='FileInfoVerbose: Подробная информация о файле',
    json_schema_extra=_json_schemas.verbose_info.docs_dump()
)

storage = ModelDocsParams(
    title='StorageUsageInfo: Использование хранилища',
    json_schema_extra=_json_schemas.storage.docs_dump()
)
