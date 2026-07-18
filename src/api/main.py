from fastapi import FastAPI

from src.api.exception_handlers import register_exception_handlers
from src.api.routes import router
from src.utils.logger import get_logger


logger = get_logger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Resume Screening AI",
        version="1.0.0",
    )

    register_exception_handlers(app)
    app.include_router(router)

    logger.info("FastAPI application initialized.")

    return app


app = create_app()
