from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from src.application.commands.create_settlement import CreateSettlementCommand
from src.domain.entities.group import GroupMember
from src.domain.entities.settlement import Settlement, SettlementStatus
from src.domain.entities.user import User
from src.domain.exceptions import ForbiddenError, NotFoundError


@pytest.fixture
def settlement_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def user_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def group_repo() -> AsyncMock:
    return AsyncMock()


class TestCreateSettlement:
    @pytest.mark.asyncio
    async def test_create_settlement_success(
        self, settlement_repo: AsyncMock, user_repo: AsyncMock, group_repo: AsyncMock
    ) -> None:
        user_repo.get_by_id.return_value = User(
            id=2, email="b@b.com", username="bob", full_name="Bob", hashed_password="x"
        )
        settlement_repo.create.return_value = Settlement(
            id=1, payer_id=1, payee_id=2, amount=Decimal("100.00"), status=SettlementStatus.PENDING
        )

        cmd = CreateSettlementCommand(settlement_repo, user_repo, group_repo)
        result = await cmd.execute(payer_id=1, payee_id=2, amount=Decimal("100.00"))

        assert result.id == 1
        assert result.payer_id == 1
        assert result.payee_id == 2
        assert result.amount == Decimal("100.00")
        settlement_repo.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_settlement_payee_not_found(
        self, settlement_repo: AsyncMock, user_repo: AsyncMock, group_repo: AsyncMock
    ) -> None:
        user_repo.get_by_id.return_value = None

        cmd = CreateSettlementCommand(settlement_repo, user_repo, group_repo)
        with pytest.raises(NotFoundError, match="Payee not found"):
            await cmd.execute(payer_id=1, payee_id=99, amount=Decimal("50.00"))

    @pytest.mark.asyncio
    async def test_create_settlement_non_member(
        self, settlement_repo: AsyncMock, user_repo: AsyncMock, group_repo: AsyncMock
    ) -> None:
        user_repo.get_by_id.return_value = User(
            id=2, email="b@b.com", username="bob", full_name="Bob", hashed_password="x"
        )
        group_repo.get_member.side_effect = [
            GroupMember(id=1, group_id=1, user_id=1),  # payer is member
            None,  # payee is NOT a member
        ]

        cmd = CreateSettlementCommand(settlement_repo, user_repo, group_repo)
        with pytest.raises(ForbiddenError, match="Both users must be members of the group"):
            await cmd.execute(payer_id=1, payee_id=2, amount=Decimal("50.00"), group_id=1)
