from src.domain.entities.group import Group, GroupMember
from src.domain.ports.repositories.group_repository import GroupRepository


class CreateGroupCommand:
    def __init__(self, group_repo: GroupRepository) -> None:
        self._group_repo = group_repo

    async def execute(self, name: str, description: str | None, creator_id: int) -> Group:
        group = Group(id=0, name=name, description=description, created_by_id=creator_id)
        created_group = await self._group_repo.create(group)

        member = GroupMember(id=0, group_id=created_group.id, user_id=creator_id, is_admin=True)
        await self._group_repo.add_member(member)

        return await self._group_repo.get_by_id(created_group.id)  # type: ignore
