from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from app.models.expense import SplitType
from app.schemas.user import UserResponse

class ExpenseSplitBase(BaseModel):
    user_id: int
    amount: Optional[Decimal] = None
    percentage: Optional[Decimal] = None

class ExpenseSplitCreate(ExpenseSplitBase):
    pass

class ExpenseSplitResponse(ExpenseSplitBase):
    id: int
    expense_id: int
    amount: Decimal
    created_at: datetime
    user: UserResponse

    class Config:
        from_attributes = True

class ExpenseBase(BaseModel):
    title: str
    description: Optional[str] = None
    amount: Decimal
    currency: str = "INR"
    split_type: SplitType = SplitType.EQUAL

class ExpenseCreate(ExpenseBase):
    group_id: int
    splits: List[ExpenseSplitCreate]

    @validator('splits')
    def validate_splits(cls, v, values):
        if not v:
            raise ValueError('At least one split is required')
        return v

class ExpenseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[Decimal] = None
    currency: Optional[str] = None
    split_type: Optional[SplitType] = None

class ExpenseResponse(ExpenseBase):
    id: int
    group_id: int
    created_by_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: UserResponse
    splits: List[ExpenseSplitResponse] = []

    class Config:
        from_attributes = True