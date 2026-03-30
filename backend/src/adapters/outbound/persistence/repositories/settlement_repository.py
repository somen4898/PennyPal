from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.outbound.persistence.mappers.settlement_mapper import SettlementMapper
from src.adapters.outbound.persistence.models.settlement import SettlementModel
from src.domain.entities.settlement import Settlement
from src.domain.ports.repositories.settlement_repository import SettlementRepository


class SqlAlchemySettlementRepository(SettlementRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, settlement_id: int) -> Settlement | None:
        result = await self._session.execute(
            select(SettlementModel).where(SettlementModel.id == settlement_id)
        )
        model = result.scalar_one_or_none()
        return SettlementMapper.to_domain(model) if model else None

    async def create(self, settlement: Settlement) -> Settlement:
        model = SettlementMapper.to_model(settlement)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return SettlementMapper.to_domain(model)

    async def update(self, settlement: Settlement) -> Settlement:
        result = await self._session.execute(
            select(SettlementModel).where(SettlementModel.id == settlement.id)
        )
        model = result.scalar_one()
        model.description = settlement.description
        model.status = SettlementMapper.to_model(settlement).status
        model.settled_at = settlement.settled_at
        await self._session.flush()
        await self._session.refresh(model)
        return SettlementMapper.to_domain(model)

    async def delete(self, settlement_id: int) -> None:
        result = await self._session.execute(
            select(SettlementModel).where(SettlementModel.id == settlement_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()

    async def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> list[Settlement]:
        result = await self._session.execute(
            select(SettlementModel)
            .where(or_(SettlementModel.payer_id == user_id, SettlementModel.payee_id == user_id))
            .offset(skip)
            .limit(limit)
        )
        return [SettlementMapper.to_domain(m) for m in result.scalars().all()]

    async def get_by_group(
        self, group_id: int, skip: int = 0, limit: int = 100
    ) -> list[Settlement]:
        result = await self._session.execute(
            select(SettlementModel)
            .where(SettlementModel.group_id == group_id)
            .offset(skip)
            .limit(limit)
        )
        return [SettlementMapper.to_domain(m) for m in result.scalars().all()]
