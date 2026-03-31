import logging
from collections.abc import Callable, Coroutine
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import Response
from starlette.responses import StreamingResponse

from src.adapters.inbound.api.router import api_router
from src.adapters.inbound.middleware.cors import setup_cors
from src.adapters.inbound.middleware.error_handler import setup_error_handlers
from src.infrastructure.container import Container
from src.infrastructure.database import async_session_factory

logger = logging.getLogger(__name__)


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
    async def inject_container(
        request: Request,
        call_next: Callable[[Request], Coroutine[Any, Any, Response]],
    ) -> Response:
        async with async_session_factory() as session:
            request.state.container = Container(session)
            try:
                response = await call_next(request)
                # BaseHTTPMiddleware wraps the response in a StreamingResponse.
                # We must consume the body before commit/rollback so that all
                # endpoint code has fully executed.
                chunks: list[bytes] = []
                assert isinstance(response, StreamingResponse)
                async for chunk in response.body_iterator:
                    chunks.append(chunk.encode() if isinstance(chunk, str) else bytes(chunk))
                body = b"".join(chunks)
                if response.status_code < 400:
                    await session.commit()
                else:
                    await session.rollback()
                return Response(
                    content=body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type,
                )
            except Exception:
                await session.rollback()
                logger.exception(
                    "Unhandled error in request %s %s",
                    request.method,
                    request.url.path,
                )
                raise

    app.include_router(api_router, prefix="/api/v1")

    @app.get("/")
    async def root() -> dict[str, str]:
        return {"message": "Welcome to PennyPal API", "version": "1.0.0", "docs": "/docs"}

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "healthy"}

    return app
