from dataclasses import dataclass
from datetime import datetime


@dataclass
class GroupMember:
    id: int
    group_id: int
    user_id: int
    is_admin: bool = False
    joined_at: datetime | None = None


@dataclass
class Group:
    id: int
    name: str
    created_by_id: int
    description: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    members: list["GroupMember"] | None = None