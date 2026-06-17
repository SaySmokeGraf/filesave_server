"""Документация для ответов."""

from app.api.utils.swagger_docs.models import ResponseDocsParams


_S200_PAGE_DESC = """
Страница из списка пользователей.

Схема: PagedUsersPublic.
"""
s200_page = ResponseDocsParams(
    description=_S200_PAGE_DESC
)
