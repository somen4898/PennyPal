from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.adapters.outbound.persistence.mappers.group_mapper import GroupMapper, GroupMemberMapper
from src.adapters.outbound.persistence.models.group import GroupMemberModel, GroupModel
from src.domain.entities.group import Group, GroupMember
from src.domain.ports.repositories.group_repository import GroupRepository


class SqlAlchemyGroupRepository(GroupRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, group_id: int) -> Group | None:
        result = await self._session.execute(
            select(GroupModel)
            .options(selectinload(GroupModel.members))
            .where(GroupModel.id == group_id)
        )
        model = result.scalar_one_or_none()
        return GroupMapper.to_domain(model) if model else None

    async def create(self, group: Group) -> Group:
        model = GroupMapper.to_model(group)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return GroupMapper.to_domain(model)

    async def update(self, group: Group) -> Group:
        result = await self._session.execute(select(GroupModel).where(GroupModel.id == group.id))
        model = result.scalar_one()
        model.name = group.name
        model.description = group.description
        await self._session.flush()
        await self._session.refresh(model)
        return GroupMapper.to_domain(model)

    async def get_user_groups(self, user_id: int) -> list[Group]:
        result = await self._session.execute(
            select(GroupModel)
            .join(GroupMemberModel)
            .options(selectinload(GroupModel.members))
            .where(GroupMemberModel.user_id == user_id)
            .order_by(GroupModel.created_at.desc())
        )
        return [GroupMapper.to_domain(m) for m in result.scalars().all()]

    async def add_member(self, member: GroupMember) -> GroupMember:
        model = GroupMemberMapper.to_model(member)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return GroupMemberMapper.to_domain(model)

    async def remove_member(self, group_id: int, user_id: int) -> None:
        result = await self._session.execute(
            select(GroupMemberModel).where(
                GroupMemberModel.group_id == group_id,
                GroupMemberModel.user_id == user_id,
            )
        )
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()

    async def get_member(self, group_id: int, user_id: int) -> GroupMember | None:
        result = await self._session.execute(
            select(GroupMemberModel).where(
                GroupMemberModel.group_id == group_id,
                GroupMemberModel.user_id == user_id,
            )
        )
        model = result.scalar_one_or_none()
        return GroupMemberMapper.to_domain(model) if model else None

    async def get_members(self, group_id: int) -> list[GroupMember]:
        result = await self._session.execute(
            select(GroupMemberModel).where(GroupMemberModel.group_id == group_id)
        )
        return [GroupMemberMapper.to_domain(m) for m in result.scalars().all()]

    async def get_member_count(self, group_id: int) -> int:
        result = await self._session.execute(
            select(func.count())
            .select_from(GroupMemberModel)
            .where(GroupMemberModel.group_id == group_id)
        )
        return result.scalar_one()
