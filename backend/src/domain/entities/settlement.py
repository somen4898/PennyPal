from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum


class SettlementStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Settlement:
    id: int
    payer_id: int
    payee_id: int
    amount: Decimal
    status: SettlementStatus = SettlementStatus.PENDING
    currency: str = "INR"
    description: str | None = None
    group_id: int | None = None
    settled_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
