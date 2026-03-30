from unittest.mock import AsyncMock

import pytest

from src.application.commands.send_chat_message import SendChatMessageCommand
from src.domain.entities.group import Group
from src.domain.entities.user import User


@pytest.fixture
def ai_client() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def group_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def expense_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def test_user() -> User:
    return User(id=1, email="a@b.com", username="alice", full_name="Alice", hashed_password="x")


class TestSendChatMessage:
    @pytest.mark.asyncio
    async def test_chat_without_group(
        self, ai_client: AsyncMock, group_repo: AsyncMock, expense_repo: AsyncMock, test_user: User
    ) -> None:
        ai_client.send_message.return_value = "Hello!"

        cmd = SendChatMessageCommand(ai_client, group_repo, expense_repo)
        result = await cmd.execute("Hi there", test_user, group_id=None)

        assert result["response"] == "Hello!"
        ai_client.send_message.assert_called_once()

    @pytest.mark.asyncio
    async def test_chat_with_group(
        self, ai_client: AsyncMock, group_repo: AsyncMock, expense_repo: AsyncMock, test_user: User
    ) -> None:
        expense_repo.get_group_splits.return_value = []
        group_repo.get_by_id.return_value = Group(id=1, name="Trip", created_by_id=1)
        ai_client.send_message.return_value = "All settled in Trip!"

        cmd = SendChatMessageCommand(ai_client, group_repo, expense_repo)
        result = await cmd.execute("What are the balances?", test_user, group_id=1)

        assert result["response"] == "All settled in Trip!"
        expense_repo.get_group_splits.assert_called_once_with(1)
        group_repo.get_by_id.assert_called_once_with(1)
        ai_client.send_message.assert_called_once()
