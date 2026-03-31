from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, field_validator


class ExpenseSplitInput(BaseModel):
    user_id: int
    amount: Decimal | None = None
    percentage: Decimal | None = None


class ExpenseCreateRequest(BaseModel):
    title: str
    description: str | None = None
    amount: Decimal
    currency: str = "INR"
    split_type: str = "equal"
    group_id: int
    splits: list[ExpenseSplitInput]

    @field_validator("splits")
    @classmethod
    def validate_splits(cls, v: list[ExpenseSplitInput]) -> list[ExpenseSplitInput]:
        if not v:
            raise ValueError("At least one split is required")
        return v


class ExpenseUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    amount: Decimal | None = None
    currency: str | None = None


class ExpenseSplitResponse(BaseModel):
    id: int
    expense_id: int
    user_id: int
    amount: Decimal
    percentage: Decimal | None = None
    created_at: datetime | None = None


class ExpenseResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    amount: Decimal
    currency: str
    split_type: str
    group_id: int
    created_by_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    splits: list[ExpenseSplitResponse] = []
