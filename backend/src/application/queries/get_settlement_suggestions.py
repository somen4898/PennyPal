from src.domain.exceptions import ForbiddenError
from src.domain.ports.repositories.expense_repository import ExpenseRepository
from src.domain.ports.repositories.group_repository import GroupRepository
from src.domain.ports.repositories.user_repository import UserRepository
from src.domain.services.settlement_service import (
    calculate_balances_from_splits,
    generate_settlement_suggestions,
)


class GetSettlementSuggestionsQuery:
    def __init__(
        self,
        expense_repo: ExpenseRepository,
        group_repo: GroupRepository,
        user_repo: UserRepository,
    ) -> None:
        self._expense_repo = expense_repo
        self._group_repo = group_repo
        self._user_repo = user_repo

    async def execute(self, group_id: int, user_id: int) -> list[dict]:
        member = await self._group_repo.get_member(group_id, user_id)
        if not member:
            raise ForbiddenError("Not a member of this group")

        splits = await self._expense_repo.get_group_splits(group_id)
        balances = calculate_balances_from_splits(splits)
        suggestions = generate_settlement_suggestions(balances, group_id)

        all_user_ids = set()
        for s in suggestions:
            all_user_ids.add(s["payer_id"])
            all_user_ids.add(s["payee_id"])

        users = await self._user_repo.get_by_ids(list(all_user_ids))
        user_map = {u.id: u for u in users}

        result = []
        for s in suggestions:
            payer = user_map.get(s["payer_id"])
            payee = user_map.get(s["payee_id"])
            result.append(
                {
                    "payer": {
                        "id": s["payer_id"],
                        "username": payer.username if payer else "Unknown",
                        "full_name": payer.full_name if payer else "Unknown",
                    },
                    "payee": {
                        "id": s["payee_id"],
                        "username": payee.username if payee else "Unknown",
                        "full_name": payee.full_name if payee else "Unknown",
                    },
                    "amount": s["amount"],
                    "group_id": s["group_id"],
                }
            )

        return result
