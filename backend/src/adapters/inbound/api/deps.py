from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.domain.entities.user import User
from src.infrastructure.container import Container

security = HTTPBearer()
security_dep = Depends(security)  # module-level to satisfy B008


async def _get_container(request: Request) -> Container:
    container: Container = request.state.container
    return container


container_dep = Depends(_get_container)  # module-level to satisfy B008


async def _get_current_user(
    credentials: HTTPAuthorizationCredentials = security_dep,
    container: Container = container_dep,
) -> User:
    token = credentials.credentials
    email = container.auth_provider.verify_token(token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    user = await container.user_repo.get_by_email(email)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    return user


# Module-level singletons for use as FastAPI dependency defaults
get_container = container_dep
get_current_user = Depends(_get_current_user)
