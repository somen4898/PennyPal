from fastapi import FastAPI, Request

from src.adapters.inbound.api.router import api_router
from src.adapters.inbound.middleware.cors import setup_cors
from src.adapters.inbound.middleware.error_handler import setup_error_handlers
from src.infrastructure.container import Container
from src.infrastructure.database import async_session_factory


def create_app() -> FastAPI:
    app = FastAPI(
        title="PennyPal API",
        description="Expense splitting and management API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    setup_cors(app)
    setup_error_handlers(app)

    @app.middleware("http")
    async def inject_container(request: Request, call_next):
        async with async_session_factory() as session, session.begin():
            request.state.container = Container(session)
            response = await call_next(request)
            return response

    app.include_router(api_router, prefix="/api/v1")

    @app.get("/")
    async def root():
        return {"message": "Welcome to PennyPal API", "version": "1.0.0", "docs": "/docs"}

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    return app
