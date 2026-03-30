from datetime import datetime

from pydantic import BaseModel


class GroupCreateRequest(BaseModel):
    name: str
    description: str | None = None


class GroupUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None


class GroupInviteRequest(BaseModel):
    user_id: int
    is_admin: bool = False


class GroupMemberResponse(BaseModel):
    id: int
    user_id: int
    group_id: int
    is_admin: bool
    joined_at: datetime | None = None


class GroupResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    created_by_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    members: list[GroupMemberResponse] = []
