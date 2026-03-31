from src.domain.exceptions import UnauthorizedError
from src.domain.ports.auth_provider import AuthProvider
from src.domain.ports.repositories.user_repository import UserRepository


class LoginUserCommand:
    def __init__(self, user_repo: UserRepository, auth_provider: AuthProvider) -> None:
        self._user_repo = user_repo
        self._auth = auth_provider

    async def execute(self, email: str, password: str) -> dict[str, str]:
        user = await self._user_repo.get_by_email(email)
        if not user or not self._auth.verify_password(password, user.hashed_password):
            raise UnauthorizedError("Incorrect email or password")
        if not user.is_active:
            raise UnauthorizedError("Inactive user")

        token = self._auth.create_access_token(subject=user.email)
        return {"access_token": token, "token_type": "bearer"}
