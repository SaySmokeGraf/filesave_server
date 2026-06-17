"""Документация для моделей."""

import app.api.auth.managers.dbmanager._swagger_docs._json_schemas as _json_schemas
from app.api.utils.swagger_docs.models import ModelDocsParams


user_public = ModelDocsParams(
    title='UserPublic: Публичная модель пользователя',
    json_schema_extra=_json_schemas.user_public.docs_dump()
)

user_updaterights = ModelDocsParams(
    title='UserUpdateRights: Обновление прав пользователя',
    json_schema_extra=_json_schemas.user_updaterights.docs_dump()
)

paged_users_public = ModelDocsParams(
    title='PagedUsersPublic: Пагинированный список публичных пользователей',
    json_schema_extra=_json_schemas.paged_users_public.docs_dump()
)
