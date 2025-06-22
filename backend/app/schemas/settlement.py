from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models.settlement import SettlementStatus
from app.schemas.user import UserResponse

class SettlementBase(BaseModel):
    amount: Decimal
    currency: str = "INR"
    description: Optional[str] = None

class SettlementCreate(SettlementBase):
    payee_id: int
    group_id: Optional[int] = None

class SettlementUpdate(BaseModel):
    description: Optional[str] = None
    status: Optional[SettlementStatus] = None

class SettlementResponse(SettlementBase):
    id: int
    payer_id: int
    payee_id: int
    status: SettlementStatus
    group_id: Optional[int] = None
    settled_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    payer: UserResponse
    payee: UserResponse

    class Config:
        from_attributes = True