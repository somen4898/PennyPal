from src.domain.entities.group import GroupMember
from src.domain.exceptions import ConflictError, ForbiddenError, NotFoundError
from src.domain.ports.repositories.group_repository import GroupRepository
from src.domain.ports.repositories.user_repository import UserRepository


class AddGroupMemberCommand:
    def __init__(self, group_repo: GroupRepository, user_repo: UserRepository) -> None:
        self._group_repo = group_repo
        self._user_repo = user_repo

    async def execute(
        self, group_id: int, user_id: int, is_admin: bool, current_user_id: int
    ) -> GroupMember:
        group = await self._group_repo.get_by_id(group_id)
        if not group:
            raise NotFoundError("Group not found")

        admin_member = await self._group_repo.get_member(group_id, current_user_id)
        if not admin_member or not admin_member.is_admin:
            raise ForbiddenError("Only group admins can invite users")

        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        existing = await self._group_repo.get_member(group_id, user_id)
        if existing:
            raise ConflictError("User is already a member of this group")

        member = GroupMember(id=0, group_id=group_id, user_id=user_id, is_admin=is_admin)
        return await self._group_repo.add_member(member)
