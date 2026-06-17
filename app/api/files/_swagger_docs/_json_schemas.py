"""JSON-схемы для документации моделей."""

from app.api.utils.swagger_docs.models import ModelJSONSchemaParams


short_info = ModelJSONSchemaParams(
    description='Краткая информация о файле.',
    examples=[
        {'filename': 'example.txt', 'size': 556}
    ]
)

verbose_info = ModelJSONSchemaParams(
    description='Подробная информация о файле.',
    examples=[
        {'filename': 'example.txt', 'size': 556, 'content_type': 'text',
         'atime': 1645557742.0, 'mtime': 1320995471.0}
    ]
)

storage = ModelJSONSchemaParams(
    description='Информация об использовании хранилища.',
    examples=[
        {'used': 10 << 30, 'free': 100 << 30}
    ]
)
