from decimal import Decimal

from src.domain.exceptions import ForbiddenError
from src.domain.ports.repositories.expense_repository import ExpenseRepository
from src.domain.ports.repositories.group_repository import GroupRepository
from src.domain.ports.repositories.user_repository import UserRepository
from src.domain.services.settlement_service import calculate_balances_from_splits


class GetBalancesQuery:
    def __init__(
        self,
        expense_repo: ExpenseRepository,
        group_repo: GroupRepository,
        user_repo: UserRepository,
    ) -> None:
        self._expense_repo = expense_repo
        self._group_repo = group_repo
        self._user_repo = user_repo

    async def execute(self, group_id: int, user_id: int) -> dict[str, Decimal]:
        member = await self._group_repo.get_member(group_id, user_id)
        if not member:
            raise ForbiddenError("Not a member of this group")

        splits = await self._expense_repo.get_group_splits(group_id)
        balances = calculate_balances_from_splits(splits)

        users = await self._user_repo.get_by_ids(list(balances.keys()))
        user_map = {u.id: u for u in users}

        result: dict[str, Decimal] = {}
        for uid, balance in balances.items():
            user = user_map.get(uid)
            if user:
                result[user.username] = balance

        return result
