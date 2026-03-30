from decimal import Decimal

from src.domain.entities.settlement import Settlement, SettlementStatus
from src.domain.exceptions import ForbiddenError, NotFoundError
from src.domain.ports.repositories.group_repository import GroupRepository
from src.domain.ports.repositories.settlement_repository import SettlementRepository
from src.domain.ports.repositories.user_repository import UserRepository


class CreateSettlementCommand:
    def __init__(
        self,
        settlement_repo: SettlementRepository,
        user_repo: UserRepository,
        group_repo: GroupRepository,
    ) -> None:
        self._settlement_repo = settlement_repo
        self._user_repo = user_repo
        self._group_repo = group_repo

    async def execute(
        self,
        payer_id: int,
        payee_id: int,
        amount: Decimal,
        group_id: int | None = None,
        currency: str = "INR",
        description: str | None = None,
    ) -> Settlement:
        payee = await self._user_repo.get_by_id(payee_id)
        if not payee:
            raise NotFoundError("Payee not found")

        if group_id:
            payer_member = await self._group_repo.get_member(group_id, payer_id)
            payee_member = await self._group_repo.get_member(group_id, payee_id)
            if not payer_member or not payee_member:
                raise ForbiddenError("Both users must be members of the group")

        settlement = Settlement(
            id=0,
            payer_id=payer_id,
            payee_id=payee_id,
            amount=amount,
            status=SettlementStatus.PENDING,
            currency=currency,
            description=description,
            group_id=group_id,
        )
        return await self._settlement_repo.create(settlement)
