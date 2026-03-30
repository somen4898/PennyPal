from src.domain.entities.user import User
from src.domain.exceptions import ConflictError
from src.domain.ports.auth_provider import AuthProvider
from src.domain.ports.repositories.user_repository import UserRepository


class RegisterUserCommand:
    def __init__(self, user_repo: UserRepository, auth_provider: AuthProvider) -> None:
        self._user_repo = user_repo
        self._auth = auth_provider

    async def execute(self, email: str, username: str, full_name: str, password: str) -> User:
        if await self._user_repo.get_by_email(email):
            raise ConflictError("Email already registered")
        if await self._user_repo.get_by_username(username):
            raise ConflictError("Username already taken")

        hashed_password = self._auth.hash_password(password)
        user = User(
            id=0,
            email=email,
            username=username,
            full_name=full_name,
            hashed_password=hashed_password,
        )
        return await self._user_repo.create(user)
