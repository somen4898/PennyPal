from src.domain.entities.group import Group
from src.domain.ports.repositories.group_repository import GroupRepository


class GetUserGroupsQuery:
    def __init__(self, group_repo: GroupRepository) -> None:
        self._group_repo = group_repo

    async def execute(self, user_id: int) -> list[Group]:
        return await self._group_repo.get_user_groups(user_id)
