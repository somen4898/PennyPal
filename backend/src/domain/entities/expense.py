from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum


class SplitType(Enum):
    EQUAL = "equal"
    EXACT = "exact"
    PERCENTAGE = "percentage"


@dataclass
class ExpenseSplit:
    id: int
    expense_id: int
    user_id: int
    amount: Decimal
    percentage: Decimal | None = None
    created_at: datetime | None = None


@dataclass
class Expense:
    id: int
    title: str
    amount: Decimal
    group_id: int
    created_by_id: int
    split_type: SplitType = SplitType.EQUAL
    description: str | None = None
    currency: str = "INR"
    created_at: datetime | None = None
    updated_at: datetime | None = None
    splits: list[ExpenseSplit] = field(default_factory=list)
