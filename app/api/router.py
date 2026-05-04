"""Общий роутер API."""

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.api.auth.router import router as auth_router
from app.api.files.router import router as files_router
from app.config import ENDPOINT_STATIC


router = APIRouter()
router.include_router(files_router, prefix='/files', tags=['files'])
router.include_router(auth_router, prefix='/auth', tags=['authorization'])


@router.get('/', tags=['common'])
async def get_root() -> RedirectResponse:
    """Получить главное окно сервиса.

    Перенаправляет на маунт статических файлов с фронтендом.

    Returns:
        RedirectResponse: Перенаправление на фронтенд.
    """
    return RedirectResponse(ENDPOINT_STATIC)
