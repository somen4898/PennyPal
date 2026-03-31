import logging
import warnings

from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

_INSECURE_DEFAULT_KEY = "change-me-in-production"


class Settings(BaseSettings):
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/pennypal"  # pragma: allowlist secret
    )
    SECRET_KEY: str = _INSECURE_DEFAULT_KEY
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ANTHROPIC_API_KEY: str = ""
    CLAUDE_MODEL: str = "claude-sonnet-4-6"
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    ENVIRONMENT: str = "development"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

if settings.SECRET_KEY == _INSECURE_DEFAULT_KEY:
    if settings.ENVIRONMENT == "production":
        raise RuntimeError("SECRET_KEY must be changed in production. Set a strong random key.")
    warnings.warn(
        "Using insecure default SECRET_KEY. Set SECRET_KEY in .env for production.",
        stacklevel=1,
    )
