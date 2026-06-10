"""Общий роутер API.

Contains:
    router: Общий роутер API. Включает в себя все роутеры составных частей API
        и эндпоинт '/', перенаправляющий на статические файлы.
"""

from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse

import app.api._swagger_docs as swdocs
from app.api.auth.router import router as auth_router
from app.api.files.router import router as files_router
from app.api.moder.router import router as moder_router
from app.config import ENDPOINT_STATIC


router = APIRouter()
router.include_router(auth_router, prefix='/auth')
router.include_router(files_router, prefix='/files')
router.include_router(moder_router, prefix='/moder')


@router.get('/', **swdocs.get_root.docs_dump())
async def get_root() -> RedirectResponse:
    """Получить главное окно сервиса.

    Перенаправляет на маунт статических файлов с фронтендом.

    Returns:
        RedirectResponse: (308) Перенаправление на фронтенд.
    """
    return RedirectResponse(
        status_code=status.HTTP_308_PERMANENT_REDIRECT,
        url=ENDPOINT_STATIC,
    )
