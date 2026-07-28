from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from src.api.exception_handlers import register_exception_handlers
from src.api.routes import router
from src.config.paths import FRONTEND_DIR
from src.utils.logger import get_logger


logger = get_logger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Resume Screening AI",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)
    app.include_router(router)

    if FRONTEND_DIR.exists():
        app.mount(
            "/app",
            StaticFiles(directory=FRONTEND_DIR, html=True),
            name="frontend",
        )

    @app.get("/", include_in_schema=False)
    def frontend_redirect() -> RedirectResponse:
        return RedirectResponse(url="/app/")

    logger.info("FastAPI application initialized.")

    return app


app = create_app()
