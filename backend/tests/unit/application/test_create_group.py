from unittest.mock import AsyncMock

import pytest

from src.application.commands.create_group import CreateGroupCommand
from src.domain.entities.group import Group, GroupMember


@pytest.fixture
def group_repo() -> AsyncMock:
    return AsyncMock()


class TestCreateGroup:
    @pytest.mark.asyncio
    async def test_create_group_success(self, group_repo: AsyncMock) -> None:
        group_repo.create.return_value = Group(
            id=1, name="Trip", description="Goa trip", created_by_id=1
        )
        group_repo.get_by_id.return_value = Group(
            id=1,
            name="Trip",
            description="Goa trip",
            created_by_id=1,
            members=[GroupMember(id=1, group_id=1, user_id=1, is_admin=True)],
        )

        cmd = CreateGroupCommand(group_repo)
        result = await cmd.execute("Trip", "Goa trip", creator_id=1)

        assert result.name == "Trip"
        assert result.created_by_id == 1
        group_repo.create.assert_called_once()
        group_repo.get_by_id.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_create_group_adds_creator_as_admin(self, group_repo: AsyncMock) -> None:
        group_repo.create.return_value = Group(id=1, name="Trip", description=None, created_by_id=1)
        group_repo.get_by_id.return_value = Group(
            id=1, name="Trip", description=None, created_by_id=1
        )

        cmd = CreateGroupCommand(group_repo)
        await cmd.execute("Trip", None, creator_id=1)

        group_repo.add_member.assert_called_once()
        member_arg = group_repo.add_member.call_args[0][0]
        assert member_arg.is_admin is True
        assert member_arg.user_id == 1
        assert member_arg.group_id == 1
