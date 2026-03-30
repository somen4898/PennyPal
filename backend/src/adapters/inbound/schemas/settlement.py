from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class SettlementCreateRequest(BaseModel):
    payee_id: int
    amount: Decimal
    currency: str = "INR"
    description: str | None = None
    group_id: int | None = None


class SettlementUpdateRequest(BaseModel):
    description: str | None = None
    status: str | None = None


class SettlementResponse(BaseModel):
    id: int
    payer_id: int
    payee_id: int
    amount: Decimal
    currency: str
    status: str
    description: str | None = None
    group_id: int | None = None
    settled_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
