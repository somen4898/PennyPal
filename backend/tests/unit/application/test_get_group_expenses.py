from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from src.application.queries.get_group_expenses import GetGroupExpensesQuery
from src.domain.entities.expense import Expense, SplitType
from src.domain.entities.group import GroupMember
from src.domain.exceptions import ForbiddenError


@pytest.fixture
def expense_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def group_repo() -> AsyncMock:
    return AsyncMock()


class TestGetGroupExpenses:
    @pytest.mark.asyncio
    async def test_get_group_expenses_success(
        self, expense_repo: AsyncMock, group_repo: AsyncMock
    ) -> None:
        group_repo.get_member.return_value = GroupMember(
            id=1, group_id=1, user_id=1, is_admin=True
        )
        expense_repo.get_by_group.return_value = [
            Expense(
                id=1,
                title="Dinner",
                amount=Decimal("100.00"),
                group_id=1,
                created_by_id=1,
                split_type=SplitType.EQUAL,
            ),
        ]

        query = GetGroupExpensesQuery(expense_repo, group_repo)
        result = await query.execute(group_id=1, user_id=1)

        assert len(result) == 1
        assert result[0].title == "Dinner"
        assert result[0].amount == Decimal("100.00")
        group_repo.get_member.assert_called_once_with(1, 1)
        expense_repo.get_by_group.assert_called_once_with(1, 0, 100)

    @pytest.mark.asyncio
    async def test_get_group_expenses_non_member(
        self, expense_repo: AsyncMock, group_repo: AsyncMock
    ) -> None:
        group_repo.get_member.return_value = None

        query = GetGroupExpensesQuery(expense_repo, group_repo)
        with pytest.raises(ForbiddenError, match="Not a member of this group"):
            await query.execute(group_id=1, user_id=99)

        expense_repo.get_by_group.assert_not_called()
