"""Документация для заголовков."""

from app.api.utils.swagger_docs.models import HeaderDocsParams


_CONTENT_DISPOSITION_DESC = """
Заголовок, отвечающий за расположение контента в ответе.

В данном случае всегда принимает значение 'attachment' для передачи в
прикрепленном к ответу виде для скачивания файла, а не его открытия в браузере.
"""
content_disposition = HeaderDocsParams(
    description=_CONTENT_DISPOSITION_DESC,
    schema_={'type': 'string', 'example': 'attachment'},
    required=True
)
