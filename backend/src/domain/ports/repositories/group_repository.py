from abc import ABC, abstractmethod

from src.domain.entities.group import Group, GroupMember


class GroupRepository(ABC):
    @abstractmethod
    async def get_by_id(self, group_id: int) -> Group | None: ...

    @abstractmethod
    async def create(self, group: Group) -> Group: ...

    @abstractmethod
    async def update(self, group: Group) -> Group: ...

    @abstractmethod
    async def get_user_groups(self, user_id: int) -> list[Group]: ...

    @abstractmethod
    async def add_member(self, member: GroupMember) -> GroupMember: ...

    @abstractmethod
    async def remove_member(self, group_id: int, user_id: int) -> None: ...

    @abstractmethod
    async def get_member(self, group_id: int, user_id: int) -> GroupMember | None: ...

    @abstractmethod
    async def get_members(self, group_id: int) -> list[GroupMember]: ...

    @abstractmethod
    async def get_member_count(self, group_id: int) -> int: ...