from decimal import Decimal
from typing import Any

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.adapters.outbound.persistence.mappers.expense_mapper import (
    ExpenseMapper,
    ExpenseSplitMapper,
)
from src.adapters.outbound.persistence.models.expense import ExpenseModel, ExpenseSplitModel
from src.domain.entities.expense import Expense, ExpenseSplit
from src.domain.ports.repositories.expense_repository import ExpenseRepository


class SqlAlchemyExpenseRepository(ExpenseRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, expense_id: int) -> Expense | None:
        result = await self._session.execute(
            select(ExpenseModel)
            .options(selectinload(ExpenseModel.splits))
            .where(ExpenseModel.id == expense_id)
        )
        model = result.scalar_one_or_none()
        return ExpenseMapper.to_domain(model) if model else None

    async def create(self, expense: Expense) -> Expense:
        model = ExpenseMapper.to_model(expense)
        self._session.add(model)
        await self._session.flush()
        result = await self._session.execute(
            select(ExpenseModel)
            .options(selectinload(ExpenseModel.splits))
            .where(ExpenseModel.id == model.id)
        )
        model = result.scalar_one()
        return ExpenseMapper.to_domain(model)

    async def create_splits(self, splits: list[ExpenseSplit]) -> list[ExpenseSplit]:
        models = [ExpenseSplitMapper.to_model(s) for s in splits]
        self._session.add_all(models)
        await self._session.flush()
        for m in models:
            await self._session.refresh(m)
        return [ExpenseSplitMapper.to_domain(m) for m in models]

    async def update(self, expense: Expense) -> Expense:
        result = await self._session.execute(
            select(ExpenseModel).where(ExpenseModel.id == expense.id)
        )
        model = result.scalar_one()
        model.title = expense.title
        model.description = expense.description
        model.amount = expense.amount
        model.currency = expense.currency
        await self._session.flush()
        result = await self._session.execute(
            select(ExpenseModel)
            .options(selectinload(ExpenseModel.splits))
            .where(ExpenseModel.id == model.id)
        )
        model = result.scalar_one()
        return ExpenseMapper.to_domain(model)

    async def delete(self, expense_id: int) -> None:
        result = await self._session.execute(
            select(ExpenseModel)
            .options(selectinload(ExpenseModel.splits))
            .where(ExpenseModel.id == expense_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()

    async def get_by_group(self, group_id: int, skip: int = 0, limit: int = 100) -> list[Expense]:
        result = await self._session.execute(
            select(ExpenseModel)
            .options(selectinload(ExpenseModel.splits))
            .where(ExpenseModel.group_id == group_id)
            .order_by(ExpenseModel.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return [ExpenseMapper.to_domain(m) for m in result.scalars().all()]

    async def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> list[Expense]:
        result = await self._session.execute(
            select(ExpenseModel)
            .join(ExpenseSplitModel)
            .options(selectinload(ExpenseModel.splits))
            .where(
                or_(
                    ExpenseModel.created_by_id == user_id,
                    ExpenseSplitModel.user_id == user_id,
                )
            )
            .distinct()
            .offset(skip)
            .limit(limit)
        )
        return [ExpenseMapper.to_domain(m) for m in result.scalars().all()]

    async def get_group_splits(self, group_id: int) -> list[dict[str, Any]]:
        result = await self._session.execute(
            select(ExpenseSplitModel)
            .join(ExpenseModel)
            .options(selectinload(ExpenseSplitModel.expense))
            .where(ExpenseModel.group_id == group_id)
        )
        splits = []
        for model in result.scalars().all():
            splits.append(
                {
                    "expense_creator_id": model.expense.created_by_id,
                    "user_id": model.user_id,
                    "amount": Decimal(str(model.amount)),
                    "total_amount": Decimal(str(model.expense.amount)),
                }
            )
        return splits
