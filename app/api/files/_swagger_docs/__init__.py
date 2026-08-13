"""Документация для отображения в OpenAPI (Swagger) для пакета files."""

from app.api.files._swagger_docs import endpoints, fields, models, params

import app.api.utils.swagger_docs.common as swcommon
from app.api.utils.swagger_docs.models import RouterDocsParams


# роутер
router = RouterDocsParams(
    tags=['files'],
    responses={
        401: swcommon.resp_401_token.docs_dump(),
        403: swcommon.resp_403_user.docs_dump(),
        422: swcommon.resp_422_validation.docs_dump()
    }
)
