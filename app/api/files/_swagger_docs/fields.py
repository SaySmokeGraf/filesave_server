"""Документация для полей."""

from app.api.utils.swagger_docs.models import FieldDocsParams


filename = FieldDocsParams(
    title='Имя файла',
    description='Имя файла в формате <стэм>.<расширение>.',
    examples=['text.txt', 'stem.suffix', 'abc123.abc123']
)

size = FieldDocsParams(
    title='Размер файла',
    description='Размер файла в байтах.',
    examples=[0, 123456, 10 << 30]
)

_CONTENT_TYPE_DESC = """
MIME-тип содержимого или null в случае невозможности определения.
"""
content_type = FieldDocsParams(
    title='MIME-тип',
    description=_CONTENT_TYPE_DESC,
    examples=['image/jpeg', 'video/mp4', None]
)

_ATIME_DESC = """
Время последнего доступа к файлу в формате Epoch Unix Timestamp.
"""
atime = FieldDocsParams(
    title='Время последнего доступа',
    description=_ATIME_DESC,
    examples=[1645557742.0, 1320995471.0, 981493200.0]
)

_MTIME_DESC = """
Время последнего изменения файла в формате Epoch Unix Timestamp.
"""
mtime = FieldDocsParams(
    title='Время последнего изменения',
    description=_MTIME_DESC,
    examples=[1645557742.0, 1320995471.0, 981493200.0]
)

used = FieldDocsParams(
    title='Использованное место',
    description='Использованное место на диске в байтах.',
    examples=[0, 123456, 10 << 30]
)

free = FieldDocsParams(
    title='Свободное место',
    description='Свободное место на диске в байтах.',
    examples=[0, 123456, 10 << 30]
)
