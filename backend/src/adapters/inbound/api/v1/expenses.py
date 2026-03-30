from fastapi import APIRouter

from src.adapters.inbound.api.deps import get_container, get_current_user
from src.adapters.inbound.schemas.expense import (
    ExpenseCreateRequest,
    ExpenseResponse,
    ExpenseSplitResponse,
)
from src.application.commands.create_expense import CreateExpenseCommand
from src.application.queries.get_group_expenses import GetGroupExpensesQuery
from src.domain.entities.expense import Expense, SplitType
from src.domain.entities.user import User
from src.domain.exceptions import ForbiddenError, NotFoundError
from src.infrastructure.container import Container

router = APIRouter()


def _expense_response(expense: Expense) -> ExpenseResponse:
    return ExpenseResponse(
        id=expense.id,
        title=expense.title,
        description=expense.description,
        amount=expense.amount,
        currency=expense.currency,
        split_type=expense.split_type.value,
        group_id=expense.group_id,
        created_by_id=expense.created_by_id,
        created_at=expense.created_at,
        updated_at=expense.updated_at,
        splits=[
            ExpenseSplitResponse(
                id=s.id,
                expense_id=s.expense_id,
                user_id=s.user_id,
                amount=s.amount,
                percentage=s.percentage,
                created_at=s.created_at,
            )
            for s in expense.splits
        ],
    )


@router.post("/", response_model=ExpenseResponse)
async def create_expense(
    body: ExpenseCreateRequest,
    current_user: User = get_current_user,
    container: Container = get_container,
):
    split_type = SplitType(body.split_type)
    user_ids = [s.user_id for s in body.splits]
    split_amounts = [s.amount for s in body.splits if s.amount is not None] or None
    split_percentages = [s.percentage for s in body.splits if s.percentage is not None] or None

    cmd = CreateExpenseCommand(container.expense_repo, container.group_repo)
    expense = await cmd.execute(
        title=body.title,
        amount=body.amount,
        group_id=body.group_id,
        creator_id=current_user.id,
        split_type=split_type,
        user_ids=user_ids,
        description=body.description,
        currency=body.currency,
        split_amounts=split_amounts,
        split_percentages=split_percentages,
    )
    return _expense_response(expense)


@router.get("/group/{group_id}", response_model=list[ExpenseResponse])
async def get_group_expenses(
    group_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = get_current_user,
    container: Container = get_container,
):
    query = GetGroupExpensesQuery(container.expense_repo, container.group_repo)
    expenses = await query.execute(group_id, current_user.id, skip, limit)
    return [_expense_response(e) for e in expenses]


@router.get("/{expense_id}", response_model=ExpenseResponse)
async def get_expense(
    expense_id: int,
    current_user: User = get_current_user,
    container: Container = get_container,
):
    expense = await container.expense_repo.get_by_id(expense_id)
    if not expense:
        raise NotFoundError("Expense not found")
    member = await container.group_repo.get_member(expense.group_id, current_user.id)
    if not member:
        raise ForbiddenError("Not a member of this group")
    return _expense_response(expense)


@router.delete("/{expense_id}")
async def delete_expense(
    expense_id: int,
    current_user: User = get_current_user,
    container: Container = get_container,
):
    expense = await container.expense_repo.get_by_id(expense_id)
    if not expense:
        raise NotFoundError("Expense not found")
    if expense.created_by_id != current_user.id:
        raise ForbiddenError("Only the creator can delete this expense")
    await container.expense_repo.delete(expense_id)
    return {"message": "Expense deleted successfully"}
