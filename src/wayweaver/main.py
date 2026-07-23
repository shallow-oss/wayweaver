from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from wayweaver.api.router import api_router
from wayweaver.core.config import Settings, get_settings
from wayweaver.db.session import dispose_engine

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield
    await dispose_engine()


def create_app(settings:Settings | None = None) -> FastAPI:
    app_settings = settings if settings is not None else get_settings()

    application = FastAPI(
        title=app_settings.app_name,
        debug=app_settings.debug,
        lifespan=lifespan,
    ) 
    application.state.settings = app_settings
    application.include_router(api_router)
    return application

app = create_app()