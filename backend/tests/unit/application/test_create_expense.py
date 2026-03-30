from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from src.application.commands.create_expense import CreateExpenseCommand
from src.domain.entities.expense import Expense, SplitType
from src.domain.entities.group import GroupMember
from src.domain.exceptions import ForbiddenError


@pytest.fixture
def expense_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def group_repo() -> AsyncMock:
    return AsyncMock()


class TestCreateExpense:
    @pytest.mark.asyncio
    async def test_create_equal_split(self, expense_repo: AsyncMock, group_repo: AsyncMock) -> None:
        group_repo.get_member.return_value = GroupMember(id=1, group_id=1, user_id=1, is_admin=True)
        expense_repo.create.return_value = Expense(
            id=1, title="Lunch", amount=Decimal("100"), group_id=1, created_by_id=1
        )
        expense_repo.get_by_id.return_value = Expense(
            id=1, title="Lunch", amount=Decimal("100"), group_id=1, created_by_id=1
        )

        cmd = CreateExpenseCommand(expense_repo, group_repo)
        result = await cmd.execute(
            title="Lunch",
            amount=Decimal("100"),
            group_id=1,
            creator_id=1,
            split_type=SplitType.EQUAL,
            user_ids=[1, 2],
        )

        assert result.id == 1
        expense_repo.create.assert_called_once()
        expense_repo.create_splits.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_non_member_raises(self, expense_repo: AsyncMock, group_repo: AsyncMock) -> None:
        group_repo.get_member.return_value = None

        cmd = CreateExpenseCommand(expense_repo, group_repo)
        with pytest.raises(ForbiddenError, match="Not a member"):
            await cmd.execute(
                title="Lunch",
                amount=Decimal("100"),
                group_id=1,
                creator_id=999,
                split_type=SplitType.EQUAL,
                user_ids=[999, 2],
            )
