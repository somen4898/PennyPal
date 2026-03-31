from fastapi import APIRouter

from src.adapters.inbound.api.deps import get_container, get_current_user
from src.adapters.inbound.schemas.user import UserResponse, UserUpdateRequest
from src.domain.entities.user import User
from src.domain.exceptions import ConflictError
from src.infrastructure.container import Container

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = get_current_user) -> UserResponse:
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )


@router.put("/me", response_model=UserResponse)
async def update_me(
    body: UserUpdateRequest,
    current_user: User = get_current_user,
    container: Container = get_container,
) -> UserResponse:
    if body.email is not None and body.email != current_user.email:
        existing = await container.user_repo.get_by_email(body.email)
        if existing:
            raise ConflictError("Email already registered")
        current_user.email = body.email
    if body.username is not None and body.username != current_user.username:
        existing = await container.user_repo.get_by_username(body.username)
        if existing:
            raise ConflictError("Username already taken")
        current_user.username = body.username
    if body.full_name is not None:
        current_user.full_name = body.full_name
    if body.password is not None:
        current_user.hashed_password = container.auth_provider.hash_password(body.password)

    updated = await container.user_repo.update(current_user)
    return UserResponse(
        id=updated.id,
        email=updated.email,
        username=updated.username,
        full_name=updated.full_name,
        is_active=updated.is_active,
        created_at=updated.created_at,
        updated_at=updated.updated_at,
    )


@router.get("/", response_model=list[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = get_current_user,
    container: Container = get_container,
) -> list[UserResponse]:
    users = await container.user_repo.list_all(skip, limit)
    return [
        UserResponse(
            id=u.id,
            email=u.email,
            username=u.username,
            full_name=u.full_name,
            is_active=u.is_active,
            created_at=u.created_at,
            updated_at=u.updated_at,
        )
        for u in users
    ]
