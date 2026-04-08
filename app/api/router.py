"""Общий роутер API."""

from fastapi import APIRouter

from app.api.files.router import router as files_router


router = APIRouter()
router.include_router(files_router, prefix='/files', tags=['files'])


@router.get('/', tags=['common'])
async def get_root():
    return {'message': 'Hello!'}
