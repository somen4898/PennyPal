from decimal import Decimal

from src.domain.entities.expense import Expense, ExpenseSplit, SplitType
from src.domain.exceptions import ForbiddenError, ValidationError
from src.domain.ports.repositories.expense_repository import ExpenseRepository
from src.domain.ports.repositories.group_repository import GroupRepository
from src.domain.services.expense_service import calculate_splits


class CreateExpenseCommand:
    def __init__(self, expense_repo: ExpenseRepository, group_repo: GroupRepository) -> None:
        self._expense_repo = expense_repo
        self._group_repo = group_repo

    async def execute(
        self,
        title: str,
        amount: Decimal,
        group_id: int,
        creator_id: int,
        split_type: SplitType,
        user_ids: list[int],
        description: str | None = None,
        currency: str = "INR",
        split_amounts: list[Decimal] | None = None,
        split_percentages: list[Decimal] | None = None,
    ) -> Expense:
        membership = await self._group_repo.get_member(group_id, creator_id)
        if not membership:
            raise ForbiddenError("Not a member of this group")

        for uid in user_ids:
            member = await self._group_repo.get_member(group_id, uid)
            if not member:
                raise ValidationError("All users in splits must be members of the group")

        calculated = calculate_splits(
            total_amount=amount,
            split_type=split_type,
            user_ids=user_ids,
            split_amounts=split_amounts,
            split_percentages=split_percentages,
        )

        expense = Expense(
            id=0,
            title=title,
            amount=amount,
            group_id=group_id,
            created_by_id=creator_id,
            split_type=split_type,
            description=description,
            currency=currency,
        )
        created_expense = await self._expense_repo.create(expense)

        splits = [
            ExpenseSplit(
                id=0,
                expense_id=created_expense.id,
                user_id=s["user_id"],
                amount=s["amount"],
                percentage=s["percentage"],
            )
            for s in calculated
        ]
        await self._expense_repo.create_splits(splits)

        return await self._expense_repo.get_by_id(created_expense.id)  # type: ignore
