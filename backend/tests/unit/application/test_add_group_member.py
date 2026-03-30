from unittest.mock import AsyncMock

import pytest

from src.application.commands.add_group_member import AddGroupMemberCommand
from src.domain.entities.group import Group, GroupMember
from src.domain.entities.user import User
from src.domain.exceptions import ConflictError, ForbiddenError, NotFoundError


@pytest.fixture
def group_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def user_repo() -> AsyncMock:
    return AsyncMock()


class TestAddGroupMember:
    @pytest.mark.asyncio
    async def test_add_member_success(self, group_repo: AsyncMock, user_repo: AsyncMock) -> None:
        group_repo.get_by_id.return_value = Group(id=1, name="Trip", created_by_id=1)
        group_repo.get_member.side_effect = [
            GroupMember(id=1, group_id=1, user_id=1, is_admin=True),  # admin check
            None,  # existing member check
        ]
        user_repo.get_by_id.return_value = User(
            id=2, email="b@b.com", username="bob", full_name="Bob", hashed_password="x"
        )
        group_repo.add_member.return_value = GroupMember(
            id=2, group_id=1, user_id=2, is_admin=False
        )

        cmd = AddGroupMemberCommand(group_repo, user_repo)
        result = await cmd.execute(group_id=1, user_id=2, is_admin=False, current_user_id=1)

        assert result.user_id == 2
        assert result.group_id == 1
        group_repo.add_member.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_member_group_not_found(
        self, group_repo: AsyncMock, user_repo: AsyncMock
    ) -> None:
        group_repo.get_by_id.return_value = None

        cmd = AddGroupMemberCommand(group_repo, user_repo)
        with pytest.raises(NotFoundError, match="Group not found"):
            await cmd.execute(group_id=99, user_id=2, is_admin=False, current_user_id=1)

    @pytest.mark.asyncio
    async def test_add_member_not_admin(self, group_repo: AsyncMock, user_repo: AsyncMock) -> None:
        group_repo.get_by_id.return_value = Group(id=1, name="Trip", created_by_id=1)
        group_repo.get_member.return_value = GroupMember(
            id=1, group_id=1, user_id=1, is_admin=False
        )

        cmd = AddGroupMemberCommand(group_repo, user_repo)
        with pytest.raises(ForbiddenError, match="Only group admins can invite users"):
            await cmd.execute(group_id=1, user_id=2, is_admin=False, current_user_id=1)

    @pytest.mark.asyncio
    async def test_add_member_user_not_found(
        self, group_repo: AsyncMock, user_repo: AsyncMock
    ) -> None:
        group_repo.get_by_id.return_value = Group(id=1, name="Trip", created_by_id=1)
        group_repo.get_member.side_effect = [
            GroupMember(id=1, group_id=1, user_id=1, is_admin=True),  # admin check
            None,  # existing member check (won't be reached, but define for safety)
        ]
        user_repo.get_by_id.return_value = None

        cmd = AddGroupMemberCommand(group_repo, user_repo)
        with pytest.raises(NotFoundError, match="User not found"):
            await cmd.execute(group_id=1, user_id=99, is_admin=False, current_user_id=1)

    @pytest.mark.asyncio
    async def test_add_member_duplicate(self, group_repo: AsyncMock, user_repo: AsyncMock) -> None:
        group_repo.get_by_id.return_value = Group(id=1, name="Trip", created_by_id=1)
        group_repo.get_member.side_effect = [
            GroupMember(id=1, group_id=1, user_id=1, is_admin=True),  # admin check
            GroupMember(id=2, group_id=1, user_id=2, is_admin=False),  # existing member
        ]
        user_repo.get_by_id.return_value = User(
            id=2, email="b@b.com", username="bob", full_name="Bob", hashed_password="x"
        )

        cmd = AddGroupMemberCommand(group_repo, user_repo)
        with pytest.raises(ConflictError, match="User is already a member of this group"):
            await cmd.execute(group_id=1, user_id=2, is_admin=False, current_user_id=1)
