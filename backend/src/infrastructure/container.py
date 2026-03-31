from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.outbound.ai.claude_client import ClaudeClient
from src.adapters.outbound.auth.jwt_provider import JwtAuthProvider
from src.adapters.outbound.persistence.repositories.expense_repository import (
    SqlAlchemyExpenseRepository,
)
from src.adapters.outbound.persistence.repositories.group_repository import (
    SqlAlchemyGroupRepository,
)
from src.adapters.outbound.persistence.repositories.settlement_repository import (
    SqlAlchemySettlementRepository,
)
from src.adapters.outbound.persistence.repositories.user_repository import SqlAlchemyUserRepository
from src.infrastructure.config import settings

# Singletons — stateless services created once at module import
auth_provider = JwtAuthProvider(
    secret_key=settings.SECRET_KEY,
    algorithm=settings.ALGORITHM,
    expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
)
ai_client = ClaudeClient(
    api_key=settings.ANTHROPIC_API_KEY,
    model=settings.CLAUDE_MODEL,
)


class Container:
    def __init__(self, session: AsyncSession) -> None:
        self.user_repo = SqlAlchemyUserRepository(session)
        self.group_repo = SqlAlchemyGroupRepository(session)
        self.expense_repo = SqlAlchemyExpenseRepository(session)
        self.settlement_repo = SqlAlchemySettlementRepository(session)
        self.auth_provider = auth_provider
        self.ai_client = ai_client
