from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.domain.entities.expense import Expense, ExpenseSplit, SplitType
from src.domain.entities.group import Group, GroupMember
from src.domain.entities.settlement import Settlement, SettlementStatus
from src.domain.entities.user import User


@pytest.fixture
def test_user() -> User:
    return User(
        id=1,
        email="alice@example.com",
        username="alice",
        full_name="Alice Smith",
        hashed_password="hashed_pw",
        is_active=True,
    )


@pytest.fixture
def test_user_2() -> User:
    return User(
        id=2,
        email="bob@example.com",
        username="bob",
        full_name="Bob Jones",
        hashed_password="hashed_pw",
        is_active=True,
    )


@pytest.fixture
def test_group() -> Group:
    return Group(
        id=1,
        name="Trip",
        description="Road trip",
        created_by_id=1,
        members=[
            GroupMember(id=1, group_id=1, user_id=1, is_admin=True),
            GroupMember(id=2, group_id=1, user_id=2, is_admin=False),
        ],
    )


@pytest.fixture
def test_expense() -> Expense:
    return Expense(
        id=1,
        title="Lunch",
        amount=Decimal("100.00"),
        group_id=1,
        created_by_id=1,
        split_type=SplitType.EQUAL,
        currency="INR",
        splits=[
            ExpenseSplit(id=1, expense_id=1, user_id=1, amount=Decimal("50.00")),
            ExpenseSplit(id=2, expense_id=1, user_id=2, amount=Decimal("50.00")),
        ],
    )


@pytest.fixture
def test_settlement() -> Settlement:
    return Settlement(
        id=1,
        payer_id=2,
        payee_id=1,
        amount=Decimal("50.00"),
        status=SettlementStatus.PENDING,
        currency="INR",
        group_id=1,
    )


@pytest.fixture
def mock_container(test_user, test_user_2, test_group, test_expense, test_settlement):
    """Create a mock Container with pre-configured repositories."""
    container = MagicMock()

    # User repo
    container.user_repo = AsyncMock()
    container.user_repo.get_by_id.side_effect = lambda uid: {
        1: test_user,
        2: test_user_2,
    }.get(uid)
    container.user_repo.get_by_email.side_effect = lambda email: {
        "alice@example.com": test_user,
        "bob@example.com": test_user_2,
    }.get(email)
    container.user_repo.get_by_username.return_value = None
    container.user_repo.create.side_effect = lambda u: u
    container.user_repo.update.side_effect = lambda u: u
    container.user_repo.list_all.return_value = [test_user, test_user_2]
    container.user_repo.get_by_ids.return_value = [test_user, test_user_2]

    # Group repo
    container.group_repo = AsyncMock()
    container.group_repo.get_by_id.return_value = test_group
    container.group_repo.create.side_effect = lambda g: Group(
        id=1,
        name=g.name,
        description=g.description,
        created_by_id=g.created_by_id,
    )
    container.group_repo.get_user_groups.return_value = [test_group]
    container.group_repo.get_member.return_value = GroupMember(
        id=1, group_id=1, user_id=1, is_admin=True
    )
    container.group_repo.add_member.side_effect = lambda m: m
    container.group_repo.get_members.return_value = test_group.members

    # Expense repo
    container.expense_repo = AsyncMock()
    container.expense_repo.get_by_id.return_value = test_expense
    container.expense_repo.create.side_effect = lambda e: Expense(
        id=1,
        title=e.title,
        amount=e.amount,
        group_id=e.group_id,
        created_by_id=e.created_by_id,
        split_type=e.split_type,
    )
    container.expense_repo.create_splits.return_value = test_expense.splits
    container.expense_repo.get_by_group.return_value = [test_expense]
    container.expense_repo.get_group_splits.return_value = [
        {
            "expense_creator_id": 1,
            "user_id": 1,
            "amount": Decimal("50"),
            "total_amount": Decimal("100"),
        },
        {
            "expense_creator_id": 1,
            "user_id": 2,
            "amount": Decimal("50"),
            "total_amount": Decimal("100"),
        },
    ]

    # Settlement repo
    container.settlement_repo = AsyncMock()
    container.settlement_repo.get_by_id.return_value = test_settlement
    container.settlement_repo.create.side_effect = lambda s: Settlement(
        id=1,
        payer_id=s.payer_id,
        payee_id=s.payee_id,
        amount=s.amount,
        status=s.status,
        currency=s.currency,
        group_id=s.group_id,
    )
    container.settlement_repo.update.side_effect = lambda s: s
    container.settlement_repo.get_by_user.return_value = [test_settlement]
    container.settlement_repo.get_by_group.return_value = [test_settlement]

    # Auth provider
    container.auth_provider = MagicMock()
    container.auth_provider.hash_password.return_value = "hashed_pw"
    container.auth_provider.verify_password.return_value = True
    container.auth_provider.create_access_token.return_value = "test_token_123"
    container.auth_provider.verify_token.return_value = "alice@example.com"

    # AI client
    container.ai_client = AsyncMock()
    container.ai_client.send_message.return_value = "Hello! How can I help?"

    return container
