from unittest.mock import AsyncMock

import pytest

from src.application.commands.register_user import RegisterUserCommand
from src.domain.entities.user import User
from src.domain.exceptions import ConflictError


@pytest.fixture
def user_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def auth_provider() -> AsyncMock:
    mock = AsyncMock()
    mock.hash_password.return_value = "hashed_pw"
    return mock


class TestRegisterUser:
    @pytest.mark.asyncio
    async def test_register_success(self, user_repo: AsyncMock, auth_provider: AsyncMock) -> None:
        user_repo.get_by_email.return_value = None
        user_repo.get_by_username.return_value = None
        user_repo.create.return_value = User(
            id=1, email="a@b.com", username="alice", full_name="Alice", hashed_password="hashed_pw"
        )

        cmd = RegisterUserCommand(user_repo, auth_provider)
        result = await cmd.execute("a@b.com", "alice", "Alice", "pass123")

        assert result.id == 1
        assert result.email == "a@b.com"
        user_repo.create.assert_called_once()
        auth_provider.hash_password.assert_called_once_with("pass123")

    @pytest.mark.asyncio
    async def test_register_duplicate_email(
        self, user_repo: AsyncMock, auth_provider: AsyncMock
    ) -> None:
        user_repo.get_by_email.return_value = User(
            id=1, email="a@b.com", username="alice", full_name="Alice", hashed_password="x"
        )

        cmd = RegisterUserCommand(user_repo, auth_provider)
        with pytest.raises(ConflictError, match="Email already registered"):
            await cmd.execute("a@b.com", "bob", "Bob", "pass123")
