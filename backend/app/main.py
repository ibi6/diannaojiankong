from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.exceptions import AppError, app_error_handler
from app.modules.auth.router import router as auth_router
from app.modules.system.router import router as system_router


def create_app() -> FastAPI:
    settings = get_settings()
    fastapi_app = FastAPI(title="Smart Resume Python")
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    fastapi_app.add_exception_handler(AppError, app_error_handler)
    fastapi_app.include_router(system_router, prefix="/api")
    fastapi_app.include_router(auth_router, prefix="/api")
    return fastapi_app


app = create_app()
