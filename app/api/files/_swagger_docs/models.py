"""Документация для моделей."""

from app.api.utils.swagger_docs.models import (
    ModelDocsParams, ModelJSONSchemaParams
)


short_info = ModelDocsParams(
    title='FileInfoShort: Краткая информация о файле',
    json_schema_extra=ModelJSONSchemaParams(
        description='Краткая информация о файле.',
        examples=[
            {'filename': 'example.txt', 'size': 556}
        ]
    ).docs_dump()
)

verbose_info = ModelDocsParams(
    title='FileInfoVerbose: Подробная информация о файле',
    json_schema_extra=ModelJSONSchemaParams(
        description='Подробная информация о файле.',
        examples=[
            {'filename': 'example.txt', 'size': 556, 'content_type': 'text',
             'atime': 1645557742.0, 'mtime': 1320995471.0}
        ]
    ).docs_dump()
)

storage = ModelDocsParams(
    title='StorageUsageInfo: Использование хранилища',
    json_schema_extra=ModelJSONSchemaParams(
        description='Информация об использовании хранилища.',
        examples=[
            {'used': 10 << 30, 'free': 100 << 30}
        ]
    ).docs_dump()
)
