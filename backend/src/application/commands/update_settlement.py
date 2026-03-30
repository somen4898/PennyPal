from datetime import UTC, datetime

from src.domain.entities.settlement import SettlementStatus
from src.domain.exceptions import ForbiddenError, NotFoundError
from src.domain.ports.repositories.settlement_repository import SettlementRepository


class UpdateSettlementCommand:
    def __init__(self, settlement_repo: SettlementRepository) -> None:
        self._settlement_repo = settlement_repo

    async def execute(
        self,
        settlement_id: int,
        current_user_id: int,
        description: str | None = None,
        status: SettlementStatus | None = None,
    ):
        settlement = await self._settlement_repo.get_by_id(settlement_id)
        if not settlement:
            raise NotFoundError("Settlement not found")

        if settlement.payer_id != current_user_id and settlement.payee_id != current_user_id:
            raise ForbiddenError("Only payer or payee can update this settlement")

        if description is not None:
            settlement.description = description
        if status is not None:
            settlement.status = status
            if status == SettlementStatus.COMPLETED:
                settlement.settled_at = datetime.now(UTC)

        return await self._settlement_repo.update(settlement)
