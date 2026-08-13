"""Документация для отображения в OpenAPI (Swagger) для пакета auth."""

from app.api.auth._swagger_docs import endpoints, fields, models

import app.api.utils.swagger_docs.common as swcommon
from app.api.utils.swagger_docs.models import RouterDocsParams


# роутер
router = RouterDocsParams(
    tags=['authorization'],
    responses={
        422: swcommon.resp_422_validation.docs_dump(),
    }
)
