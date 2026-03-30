from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from src.application.commands.update_settlement import UpdateSettlementCommand
from src.domain.entities.settlement import Settlement, SettlementStatus
from src.domain.exceptions import ForbiddenError, NotFoundError


@pytest.fixture
def settlement_repo() -> AsyncMock:
    return AsyncMock()


class TestUpdateSettlement:
    @pytest.mark.asyncio
    async def test_update_description(self, settlement_repo: AsyncMock) -> None:
        settlement = Settlement(
            id=1, payer_id=1, payee_id=2, amount=Decimal("100.00"), description="old"
        )
        settlement_repo.get_by_id.return_value = settlement
        settlement_repo.update.return_value = settlement

        cmd = UpdateSettlementCommand(settlement_repo)
        result = await cmd.execute(settlement_id=1, current_user_id=1, description="new desc")

        assert result.description == "new desc"
        settlement_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_status_completed(self, settlement_repo: AsyncMock) -> None:
        settlement = Settlement(id=1, payer_id=1, payee_id=2, amount=Decimal("100.00"))
        settlement_repo.get_by_id.return_value = settlement
        settlement_repo.update.return_value = settlement

        cmd = UpdateSettlementCommand(settlement_repo)
        await cmd.execute(settlement_id=1, current_user_id=1, status=SettlementStatus.COMPLETED)

        assert settlement.status == SettlementStatus.COMPLETED
        assert settlement.settled_at is not None
        settlement_repo.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_non_participant(self, settlement_repo: AsyncMock) -> None:
        settlement_repo.get_by_id.return_value = Settlement(
            id=1, payer_id=1, payee_id=2, amount=Decimal("100.00")
        )

        cmd = UpdateSettlementCommand(settlement_repo)
        with pytest.raises(ForbiddenError, match="Only payer or payee can update this settlement"):
            await cmd.execute(settlement_id=1, current_user_id=99, description="hacked")

    @pytest.mark.asyncio
    async def test_update_not_found(self, settlement_repo: AsyncMock) -> None:
        settlement_repo.get_by_id.return_value = None

        cmd = UpdateSettlementCommand(settlement_repo)
        with pytest.raises(NotFoundError, match="Settlement not found"):
            await cmd.execute(settlement_id=99, current_user_id=1, description="nope")
