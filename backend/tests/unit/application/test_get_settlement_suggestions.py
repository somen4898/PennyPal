from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from src.application.queries.get_settlement_suggestions import GetSettlementSuggestionsQuery
from src.domain.entities.group import GroupMember
from src.domain.entities.user import User
from src.domain.exceptions import ForbiddenError


@pytest.fixture
def expense_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def group_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def user_repo() -> AsyncMock:
    return AsyncMock()


class TestGetSettlementSuggestions:
    @pytest.mark.asyncio
    async def test_get_suggestions_success(
        self, expense_repo: AsyncMock, group_repo: AsyncMock, user_repo: AsyncMock
    ) -> None:
        group_repo.get_member.return_value = GroupMember(
            id=1, group_id=1, user_id=1, is_admin=True
        )
        expense_repo.get_group_splits.return_value = [
            {
                "expense_creator_id": 1,
                "user_id": 1,
                "amount": Decimal("50"),
                "total_amount": Decimal("100"),
            },
            {
                "expense_creator_id": 1,
                "user_id": 2,
                "amount": Decimal("50"),
                "total_amount": Decimal("100"),
            },
        ]
        user_repo.get_by_ids.return_value = [
            User(id=1, email="alice@example.com", username="alice", full_name="Alice", hashed_password="x"),
            User(id=2, email="bob@example.com", username="bob", full_name="Bob", hashed_password="x"),
        ]

        query = GetSettlementSuggestionsQuery(expense_repo, group_repo, user_repo)
        result = await query.execute(group_id=1, user_id=1)

        assert len(result) == 1
        suggestion = result[0]
        assert suggestion["payer"]["id"] == 2
        assert suggestion["payer"]["username"] == "bob"
        assert suggestion["payee"]["id"] == 1
        assert suggestion["payee"]["username"] == "alice"
        assert suggestion["amount"] == Decimal("50")
        assert suggestion["group_id"] == 1
        group_repo.get_member.assert_called_once_with(1, 1)
        expense_repo.get_group_splits.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_suggestions_non_member(
        self, expense_repo: AsyncMock, group_repo: AsyncMock, user_repo: AsyncMock
    ) -> None:
        group_repo.get_member.return_value = None

        query = GetSettlementSuggestionsQuery(expense_repo, group_repo, user_repo)
        with pytest.raises(ForbiddenError, match="Not a member of this group"):
            await query.execute(group_id=1, user_id=99)

        expense_repo.get_group_splits.assert_not_called()
