"""Главная точка входа в приложение."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import ENDPOINT_STATIC, PATH_STATIC
from app.api.router import router


app = FastAPI()
app.include_router(router)
app.mount(ENDPOINT_STATIC, StaticFiles(directory=PATH_STATIC, html=True))
