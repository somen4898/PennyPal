from unittest.mock import AsyncMock, MagicMock

import pytest

from src.application.commands.login_user import LoginUserCommand
from src.domain.entities.user import User
from src.domain.exceptions import UnauthorizedError


@pytest.fixture
def user_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def auth_provider() -> MagicMock:
    return MagicMock()


class TestLoginUser:
    @pytest.mark.asyncio
    async def test_login_success(self, user_repo: AsyncMock, auth_provider: MagicMock) -> None:
        user_repo.get_by_email.return_value = User(
            id=1, email="a@b.com", username="alice", full_name="Alice", hashed_password="x"
        )
        auth_provider.verify_password.return_value = True
        auth_provider.create_access_token.return_value = "tok123"

        cmd = LoginUserCommand(user_repo, auth_provider)
        result = await cmd.execute("a@b.com", "pass123")

        assert result["access_token"] == "tok123"
        assert result["token_type"] == "bearer"
        auth_provider.verify_password.assert_called_once_with("pass123", "x")
        auth_provider.create_access_token.assert_called_once_with(subject="a@b.com")

    @pytest.mark.asyncio
    async def test_login_wrong_password(
        self, user_repo: AsyncMock, auth_provider: MagicMock
    ) -> None:
        user_repo.get_by_email.return_value = User(
            id=1, email="a@b.com", username="alice", full_name="Alice", hashed_password="x"
        )
        auth_provider.verify_password.return_value = False

        cmd = LoginUserCommand(user_repo, auth_provider)
        with pytest.raises(UnauthorizedError, match="Incorrect email or password"):
            await cmd.execute("a@b.com", "wrong")

    @pytest.mark.asyncio
    async def test_login_nonexistent_email(
        self, user_repo: AsyncMock, auth_provider: MagicMock
    ) -> None:
        user_repo.get_by_email.return_value = None

        cmd = LoginUserCommand(user_repo, auth_provider)
        with pytest.raises(UnauthorizedError, match="Incorrect email or password"):
            await cmd.execute("nobody@b.com", "pass123")

    @pytest.mark.asyncio
    async def test_login_inactive_user(
        self, user_repo: AsyncMock, auth_provider: MagicMock
    ) -> None:
        user_repo.get_by_email.return_value = User(
            id=1,
            email="a@b.com",
            username="alice",
            full_name="Alice",
            hashed_password="x",
            is_active=False,
        )
        auth_provider.verify_password.return_value = True

        cmd = LoginUserCommand(user_repo, auth_provider)
        with pytest.raises(UnauthorizedError, match="Inactive user"):
            await cmd.execute("a@b.com", "pass123")
