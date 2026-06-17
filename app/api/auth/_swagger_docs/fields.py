"""Документация для полей."""

from app.api.utils.swagger_docs.models import FieldDocsParams


access_token = FieldDocsParams(
    title='Токен',
    description='Токен.',
    examples=['someAC.CESStoken.JWT', 's0meotH3r.ACC3ssT0K3N.B3Ar3rJWT']
)

token_type = FieldDocsParams(
    title='Тип токена',
    description='Тип токена.',
    examples=['bearer']
)
