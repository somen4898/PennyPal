from fastapi import APIRouter

from src.adapters.inbound.api.deps import get_container
from src.adapters.inbound.schemas.user import (
    TokenResponse,
    UserCreateRequest,
    UserLoginRequest,
    UserResponse,
)
from src.application.commands.login_user import LoginUserCommand
from src.application.commands.register_user import RegisterUserCommand
from src.infrastructure.container import Container

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(body: UserCreateRequest, container: Container = get_container):
    cmd = RegisterUserCommand(container.user_repo, container.auth_provider)
    user = await cmd.execute(body.email, body.username, body.full_name, body.password)
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.post("/login", response_model=TokenResponse)
async def login(body: UserLoginRequest, container: Container = get_container):
    cmd = LoginUserCommand(container.user_repo, container.auth_provider)
    result = await cmd.execute(body.email, body.password)
    return TokenResponse(**result)
