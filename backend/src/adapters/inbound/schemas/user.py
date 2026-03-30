from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreateRequest(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    password: str


class UserUpdateRequest(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    full_name: str | None = None
    password: str | None = None


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    is_active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
