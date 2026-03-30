from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.domain.exceptions import (
    ConflictError,
    DomainError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)

_STATUS_MAP = {
    NotFoundError: 404,
    UnauthorizedError: 401,
    ForbiddenError: 403,
    ValidationError: 400,
    ConflictError: 409,
}


def setup_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
        status_code = _STATUS_MAP.get(type(exc), 400)
        return JSONResponse(status_code=status_code, content={"detail": exc.message})
