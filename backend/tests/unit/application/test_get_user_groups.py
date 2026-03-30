from unittest.mock import AsyncMock

import pytest

from src.application.queries.get_user_groups import GetUserGroupsQuery
from src.domain.entities.group import Group


@pytest.fixture
def group_repo() -> AsyncMock:
    return AsyncMock()


class TestGetUserGroups:
    @pytest.mark.asyncio
    async def test_get_user_groups_returns_groups(self, group_repo: AsyncMock) -> None:
        group_repo.get_user_groups.return_value = [
            Group(id=1, name="Trip", created_by_id=1),
        ]

        query = GetUserGroupsQuery(group_repo)
        result = await query.execute(user_id=1)

        assert len(result) == 1
        assert result[0].name == "Trip"
        group_repo.get_user_groups.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_user_groups_empty(self, group_repo: AsyncMock) -> None:
        group_repo.get_user_groups.return_value = []

        query = GetUserGroupsQuery(group_repo)
        result = await query.execute(user_id=1)

        assert result == []
        group_repo.get_user_groups.assert_called_once_with(1)
