from decimal import Decimal
from typing import Any

from fastapi import APIRouter

from src.adapters.inbound.api.deps import get_container, get_current_user
from src.adapters.inbound.schemas.settlement import (
    SettlementCreateRequest,
    SettlementResponse,
    SettlementUpdateRequest,
)
from src.application.commands.create_settlement import CreateSettlementCommand
from src.application.commands.update_settlement import UpdateSettlementCommand
from src.application.queries.get_balances import GetBalancesQuery
from src.application.queries.get_settlement_suggestions import GetSettlementSuggestionsQuery
from src.domain.entities.settlement import Settlement, SettlementStatus
from src.domain.entities.user import User
from src.domain.exceptions import ForbiddenError, NotFoundError, ValidationError
from src.infrastructure.container import Container

router = APIRouter()


def _settlement_response(s: Settlement) -> SettlementResponse:
    return SettlementResponse(
        id=s.id,
        payer_id=s.payer_id,
        payee_id=s.payee_id,
        amount=s.amount,
        currency=s.currency,
        status=s.status.value,
        description=s.description,
        group_id=s.group_id,
        settled_at=s.settled_at,
        created_at=s.created_at,
        updated_at=s.updated_at,
    )


@router.post("/", response_model=SettlementResponse)
async def create_settlement(
    body: SettlementCreateRequest,
    current_user: User = get_current_user,
    container: Container = get_container,
) -> SettlementResponse:
    cmd = CreateSettlementCommand(
        container.settlement_repo, container.user_repo, container.group_repo
    )
    settlement = await cmd.execute(
        payer_id=current_user.id,
        payee_id=body.payee_id,
        amount=body.amount,
        group_id=body.group_id,
        currency=body.currency,
        description=body.description,
    )
    return _settlement_response(settlement)


@router.get("/", response_model=list[SettlementResponse])
async def list_settlements(
    skip: int = 0,
    limit: int = 100,
    current_user: User = get_current_user,
    container: Container = get_container,
) -> list[SettlementResponse]:
    settlements = await container.settlement_repo.get_by_user(current_user.id, skip, limit)
    return [_settlement_response(s) for s in settlements]


@router.get("/group/{group_id}/balances")
async def get_group_balances(
    group_id: int,
    current_user: User = get_current_user,
    container: Container = get_container,
) -> dict[str, Decimal]:
    query = GetBalancesQuery(container.expense_repo, container.group_repo, container.user_repo)
    return await query.execute(group_id, current_user.id)


@router.get("/group/{group_id}/suggestions")
async def get_suggestions(
    group_id: int,
    current_user: User = get_current_user,
    container: Container = get_container,
) -> list[dict[str, Any]]:
    query = GetSettlementSuggestionsQuery(
        container.expense_repo, container.group_repo, container.user_repo
    )
    return await query.execute(group_id, current_user.id)


@router.put("/{settlement_id}", response_model=SettlementResponse)
async def update_settlement(
    settlement_id: int,
    body: SettlementUpdateRequest,
    current_user: User = get_current_user,
    container: Container = get_container,
) -> SettlementResponse:
    status_enum = SettlementStatus(body.status) if body.status else None
    cmd = UpdateSettlementCommand(container.settlement_repo)
    settlement = await cmd.execute(
        settlement_id=settlement_id,
        current_user_id=current_user.id,
        description=body.description,
        status=status_enum,
    )
    return _settlement_response(settlement)


@router.delete("/{settlement_id}")
async def delete_settlement(
    settlement_id: int,
    current_user: User = get_current_user,
    container: Container = get_container,
) -> dict[str, str]:
    settlement = await container.settlement_repo.get_by_id(settlement_id)
    if not settlement:
        raise NotFoundError("Settlement not found")
    if settlement.payer_id != current_user.id:
        raise ForbiddenError("Only the payer can delete this settlement")
    if settlement.status != SettlementStatus.PENDING:
        raise ValidationError("Only pending settlements can be deleted")
    await container.settlement_repo.delete(settlement_id)
    return {"message": "Settlement deleted successfully"}
