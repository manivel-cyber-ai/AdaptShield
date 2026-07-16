from fastapi import FastAPI

from adaptshield.api.routes.health import router as health_router
from adaptshield.api.routes.conversations import router as conversations_router
from adaptshield.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version=settings.app_version)
    app.include_router(health_router)
    app.include_router(conversations_router)
    return app


app = create_app()
