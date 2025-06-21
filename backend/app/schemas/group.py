from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.user import UserResponse

class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None

class GroupCreate(GroupBase):
    pass

class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class GroupMemberResponse(BaseModel):
    id: int
    user_id: int
    group_id: int
    joined_at: datetime
    is_admin: bool
    user: UserResponse

    class Config:
        from_attributes = True

class GroupResponse(GroupBase):
    id: int
    created_by_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    members: List[GroupMemberResponse] = []

    class Config:
        from_attributes = True

class GroupInvite(BaseModel):
    user_id: int
    is_admin: bool = False