from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    email: str
    username: str
    full_name: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None