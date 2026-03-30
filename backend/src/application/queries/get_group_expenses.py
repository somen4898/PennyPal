from src.domain.entities.expense import Expense
from src.domain.exceptions import ForbiddenError
from src.domain.ports.repositories.expense_repository import ExpenseRepository
from src.domain.ports.repositories.group_repository import GroupRepository


class GetGroupExpensesQuery:
    def __init__(self, expense_repo: ExpenseRepository, group_repo: GroupRepository) -> None:
        self._expense_repo = expense_repo
        self._group_repo = group_repo

    async def execute(
        self, group_id: int, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Expense]:
        member = await self._group_repo.get_member(group_id, user_id)
        if not member:
            raise ForbiddenError("Not a member of this group")
        return await self._expense_repo.get_by_group(group_id, skip, limit)
