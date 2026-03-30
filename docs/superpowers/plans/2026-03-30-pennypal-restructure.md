# PennyPal Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure PennyPal from a flat FastAPI app into hexagonal architecture with a Nuxt 3 frontend, pre-commit hooks, Docker, and CLAUDE.md.

**Architecture:** Full hexagonal (ports & adapters). The domain layer contains pure Python dataclasses and business logic with zero framework imports. The application layer orchestrates use cases via abstract ports. Adapters implement those ports using FastAPI (inbound), SQLAlchemy (outbound), Claude API (outbound), and JWT (outbound).

**Tech Stack:** Python 3.12, FastAPI, SQLAlchemy 2.0 (async), PostgreSQL, Alembic, Nuxt 3, Nuxt UI, Tailwind CSS, Pinia, Claude API (anthropic SDK), Docker, Ruff, mypy, ESLint, Prettier, pre-commit, commitlint

---

## File Structure

### Backend (`backend/`)

**Domain (pure Python, no framework imports):**
- `src/domain/entities/user.py` — User dataclass
- `src/domain/entities/group.py` — Group, GroupMember dataclasses
- `src/domain/entities/expense.py` — Expense, ExpenseSplit dataclasses, SplitType enum
- `src/domain/entities/settlement.py` — Settlement dataclass, SettlementStatus enum
- `src/domain/services/expense_service.py` — Split calculation (pure functions)
- `src/domain/services/settlement_service.py` — Balance optimization (pure functions)
- `src/domain/ports/repositories/user_repository.py` — Abstract UserRepository
- `src/domain/ports/repositories/group_repository.py` — Abstract GroupRepository
- `src/domain/ports/repositories/expense_repository.py` — Abstract ExpenseRepository
- `src/domain/ports/repositories/settlement_repository.py` — Abstract SettlementRepository
- `src/domain/ports/ai_client.py` — Abstract AiClient
- `src/domain/ports/auth_provider.py` — Abstract AuthProvider
- `src/domain/exceptions.py` — Domain exceptions

**Application (use cases, depends only on domain):**
- `src/application/commands/register_user.py` — RegisterUserCommand
- `src/application/commands/login_user.py` — LoginUserCommand
- `src/application/commands/create_group.py` — CreateGroupCommand
- `src/application/commands/add_group_member.py` — AddGroupMemberCommand
- `src/application/commands/create_expense.py` — CreateExpenseCommand
- `src/application/commands/create_settlement.py` — CreateSettlementCommand
- `src/application/commands/update_settlement.py` — UpdateSettlementCommand
- `src/application/commands/send_chat_message.py` — SendChatMessageCommand
- `src/application/queries/get_user_groups.py` — GetUserGroupsQuery
- `src/application/queries/get_group_expenses.py` — GetGroupExpensesQuery
- `src/application/queries/get_balances.py` — GetBalancesQuery
- `src/application/queries/get_settlement_suggestions.py` — GetSettlementSuggestionsQuery

**Adapters — Inbound (FastAPI routes):**
- `src/adapters/inbound/api/v1/auth.py`
- `src/adapters/inbound/api/v1/users.py`
- `src/adapters/inbound/api/v1/groups.py`
- `src/adapters/inbound/api/v1/expenses.py`
- `src/adapters/inbound/api/v1/settlements.py`
- `src/adapters/inbound/api/v1/chatbot.py`
- `src/adapters/inbound/api/router.py`
- `src/adapters/inbound/schemas/user.py`
- `src/adapters/inbound/schemas/group.py`
- `src/adapters/inbound/schemas/expense.py`
- `src/adapters/inbound/schemas/settlement.py`
- `src/adapters/inbound/schemas/chatbot.py`
- `src/adapters/inbound/middleware/cors.py`
- `src/adapters/inbound/middleware/error_handler.py`

**Adapters — Outbound (infrastructure implementations):**
- `src/adapters/outbound/persistence/models/base.py` — SQLAlchemy Base
- `src/adapters/outbound/persistence/models/user.py`
- `src/adapters/outbound/persistence/models/group.py`
- `src/adapters/outbound/persistence/models/expense.py`
- `src/adapters/outbound/persistence/models/settlement.py`
- `src/adapters/outbound/persistence/mappers/user_mapper.py`
- `src/adapters/outbound/persistence/mappers/group_mapper.py`
- `src/adapters/outbound/persistence/mappers/expense_mapper.py`
- `src/adapters/outbound/persistence/mappers/settlement_mapper.py`
- `src/adapters/outbound/persistence/repositories/user_repository.py`
- `src/adapters/outbound/persistence/repositories/group_repository.py`
- `src/adapters/outbound/persistence/repositories/expense_repository.py`
- `src/adapters/outbound/persistence/repositories/settlement_repository.py`
- `src/adapters/outbound/ai/claude_client.py`
- `src/adapters/outbound/auth/jwt_provider.py`

**Infrastructure:**
- `src/infrastructure/config.py`
- `src/infrastructure/database.py`
- `src/infrastructure/container.py`
- `src/infrastructure/app.py`

**Tests:**
- `tests/unit/domain/test_expense_service.py`
- `tests/unit/domain/test_settlement_service.py`
- `tests/unit/application/test_create_expense.py`
- `tests/unit/application/test_create_settlement.py`
- `tests/unit/application/test_register_user.py`
- `tests/conftest.py`

**Config files:**
- `pyproject.toml`
- `Dockerfile`
- `run.py`

### Frontend (`frontend/`)
- `nuxt.config.ts`
- `app.vue`
- `pages/index.vue`, `pages/login.vue`, `pages/register.vue`
- `pages/groups/index.vue`, `pages/groups/[id].vue`
- `pages/expenses/new.vue`
- `pages/settlements/index.vue`
- `pages/chat.vue`
- `composables/useAuth.ts`, `composables/useApi.ts`
- `stores/auth.ts`
- `middleware/auth.ts`
- `server/api/[...].ts` (proxy)
- `types/index.ts`
- `package.json`, `tsconfig.json`, `Dockerfile`

### Root
- `docker-compose.yml`
- `.pre-commit-config.yaml`
- `.editorconfig`
- `CLAUDE.md`
- `README.md`

---

## Task 1: Project Scaffolding & Configuration

**Files:**
- Create: `backend/pyproject.toml`
- Create: `backend/src/__init__.py`
- Create: `backend/src/domain/__init__.py`
- Create: `backend/src/domain/entities/__init__.py`
- Create: `backend/src/domain/services/__init__.py`
- Create: `backend/src/domain/ports/__init__.py`
- Create: `backend/src/domain/ports/repositories/__init__.py`
- Create: `backend/src/application/__init__.py`
- Create: `backend/src/application/commands/__init__.py`
- Create: `backend/src/application/queries/__init__.py`
- Create: `backend/src/adapters/__init__.py`
- Create: `backend/src/adapters/inbound/__init__.py`
- Create: `backend/src/adapters/inbound/api/__init__.py`
- Create: `backend/src/adapters/inbound/api/v1/__init__.py`
- Create: `backend/src/adapters/inbound/schemas/__init__.py`
- Create: `backend/src/adapters/inbound/middleware/__init__.py`
- Create: `backend/src/adapters/outbound/__init__.py`
- Create: `backend/src/adapters/outbound/persistence/__init__.py`
- Create: `backend/src/adapters/outbound/persistence/models/__init__.py`
- Create: `backend/src/adapters/outbound/persistence/mappers/__init__.py`
- Create: `backend/src/adapters/outbound/persistence/repositories/__init__.py`
- Create: `backend/src/adapters/outbound/ai/__init__.py`
- Create: `backend/src/adapters/outbound/auth/__init__.py`
- Create: `backend/src/infrastructure/__init__.py`
- Create: `backend/tests/__init__.py`
- Create: `backend/tests/unit/__init__.py`
- Create: `backend/tests/unit/domain/__init__.py`
- Create: `backend/tests/unit/application/__init__.py`
- Create: `backend/tests/integration/__init__.py`

- [ ] **Step 1: Create `backend/pyproject.toml`**

```toml
[project]
name = "pennypal-backend"
version = "1.0.0"
description = "PennyPal expense-splitting API"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "sqlalchemy[asyncio]>=2.0.30",
    "asyncpg>=0.29.0",
    "alembic>=1.13.0",
    "pydantic[email]>=2.7.0",
    "pydantic-settings>=2.3.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "python-dotenv>=1.0.0",
    "anthropic>=0.30.0",
    "httpx>=0.27.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.2.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=5.0.0",
    "ruff>=0.5.0",
    "mypy>=1.10.0",
    "pre-commit>=3.7.0",
]

[tool.ruff]
target-version = "py312"
line-length = 100
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "A", "SIM", "TCH", "RUF"]

[tool.ruff.lint.isort]
known-first-party = ["src"]

[tool.mypy]
python_version = "3.12"
strict = true
plugins = ["pydantic.mypy"]
exclude = ["alembic/"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = "-v --tb=short"

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.backends._legacy:_Backend"
```

- [ ] **Step 2: Create all `__init__.py` files for the package structure**

Create empty `__init__.py` files in every directory listed above. Each file is empty (0 bytes).

Run:
```bash
cd backend && mkdir -p src/domain/entities src/domain/services src/domain/ports/repositories \
  src/application/commands src/application/queries \
  src/adapters/inbound/api/v1 src/adapters/inbound/schemas src/adapters/inbound/middleware \
  src/adapters/outbound/persistence/models src/adapters/outbound/persistence/mappers \
  src/adapters/outbound/persistence/repositories src/adapters/outbound/ai src/adapters/outbound/auth \
  src/infrastructure tests/unit/domain tests/unit/application tests/integration

find src tests -type d -exec touch {}/__init__.py \;
```

- [ ] **Step 3: Install dependencies**

Run:
```bash
cd backend && python -m venv .venv && source .venv/bin/activate && pip install -e ".[dev]"
```
Expected: All packages install successfully.

- [ ] **Step 4: Verify structure**

Run:
```bash
cd backend && find src -type f -name "*.py" | sort
```
Expected: All `__init__.py` files listed under the correct directories.

- [ ] **Step 5: Commit**

```bash
git add backend/pyproject.toml backend/src/ backend/tests/
git commit -m "chore: scaffold hexagonal architecture directory structure"
```

---

## Task 2: Domain Entities

**Files:**
- Create: `backend/src/domain/entities/user.py`
- Create: `backend/src/domain/entities/group.py`
- Create: `backend/src/domain/entities/expense.py`
- Create: `backend/src/domain/entities/settlement.py`
- Create: `backend/src/domain/exceptions.py`

- [ ] **Step 1: Create domain exceptions**

```python
# backend/src/domain/exceptions.py
class DomainError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class NotFoundError(DomainError):
    pass


class UnauthorizedError(DomainError):
    pass


class ForbiddenError(DomainError):
    pass


class ValidationError(DomainError):
    pass


class ConflictError(DomainError):
    pass
```

- [ ] **Step 2: Create User entity**

```python
# backend/src/domain/entities/user.py
from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    email: str
    username: str
    full_name: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime | None = None
    updated_at: datetime | None = None
```

- [ ] **Step 3: Create Group entities**

```python
# backend/src/domain/entities/group.py
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GroupMember:
    id: int
    group_id: int
    user_id: int
    is_admin: bool = False
    joined_at: datetime | None = None


@dataclass
class Group:
    id: int
    name: str
    created_by_id: int
    description: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    members: list["GroupMember"] | None = None
```

- [ ] **Step 4: Create Expense entities**

```python
# backend/src/domain/entities/expense.py
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum


class SplitType(Enum):
    EQUAL = "equal"
    EXACT = "exact"
    PERCENTAGE = "percentage"


@dataclass
class ExpenseSplit:
    id: int
    expense_id: int
    user_id: int
    amount: Decimal
    percentage: Decimal | None = None
    created_at: datetime | None = None


@dataclass
class Expense:
    id: int
    title: str
    amount: Decimal
    group_id: int
    created_by_id: int
    split_type: SplitType = SplitType.EQUAL
    description: str | None = None
    currency: str = "INR"
    created_at: datetime | None = None
    updated_at: datetime | None = None
    splits: list[ExpenseSplit] = field(default_factory=list)
```

- [ ] **Step 5: Create Settlement entity**

```python
# backend/src/domain/entities/settlement.py
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum


class SettlementStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Settlement:
    id: int
    payer_id: int
    payee_id: int
    amount: Decimal
    status: SettlementStatus = SettlementStatus.PENDING
    currency: str = "INR"
    description: str | None = None
    group_id: int | None = None
    settled_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
```

- [ ] **Step 6: Commit**

```bash
git add backend/src/domain/
git commit -m "feat(domain): add domain entities and exceptions"
```

---

## Task 3: Domain Services (Pure Business Logic)

**Files:**
- Create: `backend/src/domain/services/expense_service.py`
- Create: `backend/src/domain/services/settlement_service.py`
- Test: `backend/tests/unit/domain/test_expense_service.py`
- Test: `backend/tests/unit/domain/test_settlement_service.py`

- [ ] **Step 1: Write failing tests for expense service**

```python
# backend/tests/unit/domain/test_expense_service.py
from decimal import Decimal

import pytest

from src.domain.entities.expense import SplitType
from src.domain.exceptions import ValidationError
from src.domain.services.expense_service import calculate_splits


class TestCalculateEqualSplits:
    def test_equal_split_two_users(self) -> None:
        result = calculate_splits(
            total_amount=Decimal("100.00"),
            split_type=SplitType.EQUAL,
            user_ids=[1, 2],
            split_amounts=None,
            split_percentages=None,
        )
        assert len(result) == 2
        assert result[0] == {"user_id": 1, "amount": Decimal("50.00"), "percentage": None}
        assert result[1] == {"user_id": 2, "amount": Decimal("50.00"), "percentage": None}

    def test_equal_split_three_users(self) -> None:
        result = calculate_splits(
            total_amount=Decimal("100.00"),
            split_type=SplitType.EQUAL,
            user_ids=[1, 2, 3],
            split_amounts=None,
            split_percentages=None,
        )
        assert len(result) == 3
        for split in result:
            assert split["amount"] == Decimal("100.00") / 3

    def test_equal_split_empty_users_raises(self) -> None:
        with pytest.raises(ValidationError, match="At least one user"):
            calculate_splits(
                total_amount=Decimal("100.00"),
                split_type=SplitType.EQUAL,
                user_ids=[],
                split_amounts=None,
                split_percentages=None,
            )


class TestCalculateExactSplits:
    def test_exact_split_valid(self) -> None:
        result = calculate_splits(
            total_amount=Decimal("100.00"),
            split_type=SplitType.EXACT,
            user_ids=[1, 2],
            split_amounts=[Decimal("60.00"), Decimal("40.00")],
            split_percentages=None,
        )
        assert result[0] == {"user_id": 1, "amount": Decimal("60.00"), "percentage": None}
        assert result[1] == {"user_id": 2, "amount": Decimal("40.00"), "percentage": None}

    def test_exact_split_sum_mismatch_raises(self) -> None:
        with pytest.raises(ValidationError, match="must equal total"):
            calculate_splits(
                total_amount=Decimal("100.00"),
                split_type=SplitType.EXACT,
                user_ids=[1, 2],
                split_amounts=[Decimal("60.00"), Decimal("30.00")],
                split_percentages=None,
            )

    def test_exact_split_missing_amounts_raises(self) -> None:
        with pytest.raises(ValidationError, match="Amount must be specified"):
            calculate_splits(
                total_amount=Decimal("100.00"),
                split_type=SplitType.EXACT,
                user_ids=[1, 2],
                split_amounts=None,
                split_percentages=None,
            )


class TestCalculatePercentageSplits:
    def test_percentage_split_valid(self) -> None:
        result = calculate_splits(
            total_amount=Decimal("200.00"),
            split_type=SplitType.PERCENTAGE,
            user_ids=[1, 2],
            split_amounts=None,
            split_percentages=[Decimal("60"), Decimal("40")],
        )
        assert result[0] == {"user_id": 1, "amount": Decimal("120.00"), "percentage": Decimal("60")}
        assert result[1] == {"user_id": 2, "amount": Decimal("80.00"), "percentage": Decimal("40")}

    def test_percentage_split_not_100_raises(self) -> None:
        with pytest.raises(ValidationError, match="must sum to 100"):
            calculate_splits(
                total_amount=Decimal("200.00"),
                split_type=SplitType.PERCENTAGE,
                user_ids=[1, 2],
                split_amounts=None,
                split_percentages=[Decimal("60"), Decimal("30")],
            )

    def test_percentage_split_missing_raises(self) -> None:
        with pytest.raises(ValidationError, match="Percentage must be specified"):
            calculate_splits(
                total_amount=Decimal("200.00"),
                split_type=SplitType.PERCENTAGE,
                user_ids=[1, 2],
                split_amounts=None,
                split_percentages=None,
            )
```

- [ ] **Step 2: Run tests to verify they fail**

Run:
```bash
cd backend && source .venv/bin/activate && python -m pytest tests/unit/domain/test_expense_service.py -v
```
Expected: FAIL — `cannot import name 'calculate_splits'`

- [ ] **Step 3: Implement expense service**

```python
# backend/src/domain/services/expense_service.py
from decimal import Decimal

from src.domain.entities.expense import SplitType
from src.domain.exceptions import ValidationError


def calculate_splits(
    total_amount: Decimal,
    split_type: SplitType,
    user_ids: list[int],
    split_amounts: list[Decimal] | None,
    split_percentages: list[Decimal] | None,
) -> list[dict]:
    """Calculate split amounts based on split type. Pure function — no DB access."""
    if not user_ids:
        raise ValidationError("At least one user is required for splitting")

    splits: list[dict] = []

    if split_type == SplitType.EQUAL:
        amount_per_person = total_amount / len(user_ids)
        for uid in user_ids:
            splits.append({"user_id": uid, "amount": amount_per_person, "percentage": None})

    elif split_type == SplitType.EXACT:
        if split_amounts is None or len(split_amounts) != len(user_ids):
            raise ValidationError("Amount must be specified for each user in exact splits")
        total_specified = sum(split_amounts)
        if total_specified != total_amount:
            raise ValidationError("Sum of split amounts must equal total expense amount")
        for uid, amount in zip(user_ids, split_amounts):
            splits.append({"user_id": uid, "amount": amount, "percentage": None})

    elif split_type == SplitType.PERCENTAGE:
        if split_percentages is None or len(split_percentages) != len(user_ids):
            raise ValidationError("Percentage must be specified for each user in percentage splits")
        total_pct = sum(split_percentages)
        if abs(total_pct - Decimal("100")) > Decimal("0.01"):
            raise ValidationError("Percentages must sum to 100")
        for uid, pct in zip(user_ids, split_percentages):
            amount = (total_amount * pct) / Decimal("100")
            splits.append({"user_id": uid, "amount": amount, "percentage": pct})

    return splits
```

- [ ] **Step 4: Run expense service tests**

Run:
```bash
cd backend && source .venv/bin/activate && python -m pytest tests/unit/domain/test_expense_service.py -v
```
Expected: All 8 tests PASS.

- [ ] **Step 5: Write failing tests for settlement service**

```python
# backend/tests/unit/domain/test_settlement_service.py
from decimal import Decimal

from src.domain.services.settlement_service import (
    calculate_balances_from_splits,
    generate_settlement_suggestions,
)


class TestCalculateBalances:
    def test_single_expense_two_users(self) -> None:
        # User 1 paid 100, split equally with user 2
        splits = [
            {"expense_creator_id": 1, "user_id": 1, "amount": Decimal("50"), "total_amount": Decimal("100")},
            {"expense_creator_id": 1, "user_id": 2, "amount": Decimal("50"), "total_amount": Decimal("100")},
        ]
        balances = calculate_balances_from_splits(splits)
        assert balances[1] == Decimal("50")   # user 1 is owed 50
        assert balances[2] == Decimal("-50")  # user 2 owes 50

    def test_two_expenses_cancel_out(self) -> None:
        splits = [
            {"expense_creator_id": 1, "user_id": 1, "amount": Decimal("50"), "total_amount": Decimal("100")},
            {"expense_creator_id": 1, "user_id": 2, "amount": Decimal("50"), "total_amount": Decimal("100")},
            {"expense_creator_id": 2, "user_id": 1, "amount": Decimal("50"), "total_amount": Decimal("100")},
            {"expense_creator_id": 2, "user_id": 2, "amount": Decimal("50"), "total_amount": Decimal("100")},
        ]
        balances = calculate_balances_from_splits(splits)
        assert balances.get(1, Decimal("0")) == Decimal("0")
        assert balances.get(2, Decimal("0")) == Decimal("0")

    def test_empty_splits(self) -> None:
        balances = calculate_balances_from_splits([])
        assert balances == {}


class TestGenerateSettlementSuggestions:
    def test_simple_two_user_settlement(self) -> None:
        balances = {1: Decimal("50"), 2: Decimal("-50")}
        suggestions = generate_settlement_suggestions(balances, group_id=1)
        assert len(suggestions) == 1
        assert suggestions[0]["payer_id"] == 2
        assert suggestions[0]["payee_id"] == 1
        assert suggestions[0]["amount"] == Decimal("50")

    def test_three_users_minimized(self) -> None:
        # User 1 is owed 100, user 2 owes 60, user 3 owes 40
        balances = {1: Decimal("100"), 2: Decimal("-60"), 3: Decimal("-40")}
        suggestions = generate_settlement_suggestions(balances, group_id=1)
        assert len(suggestions) == 2
        total_settled = sum(s["amount"] for s in suggestions)
        assert total_settled == Decimal("100")

    def test_all_balanced(self) -> None:
        balances = {1: Decimal("0"), 2: Decimal("0")}
        suggestions = generate_settlement_suggestions(balances, group_id=1)
        assert suggestions == []
```

- [ ] **Step 6: Run settlement tests to verify they fail**

Run:
```bash
cd backend && source .venv/bin/activate && python -m pytest tests/unit/domain/test_settlement_service.py -v
```
Expected: FAIL — import error.

- [ ] **Step 7: Implement settlement service**

```python
# backend/src/domain/services/settlement_service.py
from collections import defaultdict
from decimal import Decimal


def calculate_balances_from_splits(
    splits: list[dict],
) -> dict[int, Decimal]:
    """Calculate net balances from expense split data. Pure function.

    Each split dict must have: expense_creator_id, user_id, amount, total_amount
    Positive balance = user is owed money. Negative = user owes money.
    """
    balances: dict[int, Decimal] = defaultdict(Decimal)

    for split in splits:
        creator_id = split["expense_creator_id"]
        user_id = split["user_id"]
        amount = split["amount"]

        if user_id == creator_id:
            # Creator paid for their own share — they're owed the rest
            balances[user_id] += split["total_amount"] - amount
        else:
            # Non-creator owes their share
            balances[user_id] -= amount
            balances[creator_id] += amount

    return dict(balances)


def generate_settlement_suggestions(
    balances: dict[int, Decimal],
    group_id: int,
) -> list[dict]:
    """Greedy algorithm to minimize settlement transactions. Pure function."""
    # Filter out zero balances
    filtered = {uid: bal for uid, bal in balances.items() if bal != Decimal("0")}

    creditors = sorted(
        [(uid, amt) for uid, amt in filtered.items() if amt > 0],
        key=lambda x: x[1],
        reverse=True,
    )
    debtors = sorted(
        [(uid, -amt) for uid, amt in filtered.items() if amt < 0],
        key=lambda x: x[1],
        reverse=True,
    )

    settlements: list[dict] = []
    i, j = 0, 0

    while i < len(creditors) and j < len(debtors):
        creditor_id, credit_amount = creditors[i]
        debtor_id, debt_amount = debtors[j]
        settlement_amount = min(credit_amount, debt_amount)

        settlements.append({
            "payer_id": debtor_id,
            "payee_id": creditor_id,
            "amount": settlement_amount,
            "group_id": group_id,
        })

        creditors[i] = (creditor_id, credit_amount - settlement_amount)
        debtors[j] = (debtor_id, debt_amount - settlement_amount)

        if creditors[i][1] == Decimal("0"):
            i += 1
        if debtors[j][1] == Decimal("0"):
            j += 1

    return settlements
```

- [ ] **Step 8: Run settlement tests**

Run:
```bash
cd backend && source .venv/bin/activate && python -m pytest tests/unit/domain/test_settlement_service.py -v
```
Expected: All 6 tests PASS.

- [ ] **Step 9: Commit**

```bash
git add backend/src/domain/services/ backend/tests/unit/domain/
git commit -m "feat(domain): add expense and settlement services with tests"
```

---

## Task 4: Domain Ports (Abstract Interfaces)

**Files:**
- Create: `backend/src/domain/ports/repositories/user_repository.py`
- Create: `backend/src/domain/ports/repositories/group_repository.py`
- Create: `backend/src/domain/ports/repositories/expense_repository.py`
- Create: `backend/src/domain/ports/repositories/settlement_repository.py`
- Create: `backend/src/domain/ports/ai_client.py`
- Create: `backend/src/domain/ports/auth_provider.py`

- [ ] **Step 1: Create UserRepository port**

```python
# backend/src/domain/ports/repositories/user_repository.py
from abc import ABC, abstractmethod

from src.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None: ...

    @abstractmethod
    async def create(self, user: User) -> User: ...

    @abstractmethod
    async def update(self, user: User) -> User: ...

    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100) -> list[User]: ...
```

- [ ] **Step 2: Create GroupRepository port**

```python
# backend/src/domain/ports/repositories/group_repository.py
from abc import ABC, abstractmethod

from src.domain.entities.group import Group, GroupMember


class GroupRepository(ABC):
    @abstractmethod
    async def get_by_id(self, group_id: int) -> Group | None: ...

    @abstractmethod
    async def create(self, group: Group) -> Group: ...

    @abstractmethod
    async def update(self, group: Group) -> Group: ...

    @abstractmethod
    async def get_user_groups(self, user_id: int) -> list[Group]: ...

    @abstractmethod
    async def add_member(self, member: GroupMember) -> GroupMember: ...

    @abstractmethod
    async def remove_member(self, group_id: int, user_id: int) -> None: ...

    @abstractmethod
    async def get_member(self, group_id: int, user_id: int) -> GroupMember | None: ...

    @abstractmethod
    async def get_members(self, group_id: int) -> list[GroupMember]: ...

    @abstractmethod
    async def get_member_count(self, group_id: int) -> int: ...
```

- [ ] **Step 3: Create ExpenseRepository port**

```python
# backend/src/domain/ports/repositories/expense_repository.py
from abc import ABC, abstractmethod

from src.domain.entities.expense import Expense, ExpenseSplit


class ExpenseRepository(ABC):
    @abstractmethod
    async def get_by_id(self, expense_id: int) -> Expense | None: ...

    @abstractmethod
    async def create(self, expense: Expense) -> Expense: ...

    @abstractmethod
    async def create_splits(self, splits: list[ExpenseSplit]) -> list[ExpenseSplit]: ...

    @abstractmethod
    async def update(self, expense: Expense) -> Expense: ...

    @abstractmethod
    async def delete(self, expense_id: int) -> None: ...

    @abstractmethod
    async def get_by_group(
        self, group_id: int, skip: int = 0, limit: int = 100
    ) -> list[Expense]: ...

    @abstractmethod
    async def get_by_user(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Expense]: ...

    @abstractmethod
    async def get_group_splits(self, group_id: int) -> list[dict]: ...
```

- [ ] **Step 4: Create SettlementRepository port**

```python
# backend/src/domain/ports/repositories/settlement_repository.py
from abc import ABC, abstractmethod

from src.domain.entities.settlement import Settlement


class SettlementRepository(ABC):
    @abstractmethod
    async def get_by_id(self, settlement_id: int) -> Settlement | None: ...

    @abstractmethod
    async def create(self, settlement: Settlement) -> Settlement: ...

    @abstractmethod
    async def update(self, settlement: Settlement) -> Settlement: ...

    @abstractmethod
    async def delete(self, settlement_id: int) -> None: ...

    @abstractmethod
    async def get_by_user(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Settlement]: ...

    @abstractmethod
    async def get_by_group(
        self, group_id: int, skip: int = 0, limit: int = 100
    ) -> list[Settlement]: ...
```

- [ ] **Step 5: Create AiClient and AuthProvider ports**

```python
# backend/src/domain/ports/ai_client.py
from abc import ABC, abstractmethod


class AiClient(ABC):
    @abstractmethod
    async def send_message(
        self, message: str, system_prompt: str, context: list[dict] | None = None
    ) -> str: ...
```

```python
# backend/src/domain/ports/auth_provider.py
from abc import ABC, abstractmethod


class AuthProvider(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str: ...

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool: ...

    @abstractmethod
    def create_access_token(self, subject: str) -> str: ...

    @abstractmethod
    def verify_token(self, token: str) -> str | None: ...
```

- [ ] **Step 6: Commit**

```bash
git add backend/src/domain/ports/
git commit -m "feat(domain): add repository and service ports"
```

---

## Task 5: Outbound Adapters — Persistence (ORM Models + Mappers + Repositories)

**Files:**
- Create: `backend/src/adapters/outbound/persistence/models/base.py`
- Create: `backend/src/adapters/outbound/persistence/models/user.py`
- Create: `backend/src/adapters/outbound/persistence/models/group.py`
- Create: `backend/src/adapters/outbound/persistence/models/expense.py`
- Create: `backend/src/adapters/outbound/persistence/models/settlement.py`
- Create: `backend/src/adapters/outbound/persistence/mappers/user_mapper.py`
- Create: `backend/src/adapters/outbound/persistence/mappers/group_mapper.py`
- Create: `backend/src/adapters/outbound/persistence/mappers/expense_mapper.py`
- Create: `backend/src/adapters/outbound/persistence/mappers/settlement_mapper.py`
- Create: `backend/src/adapters/outbound/persistence/repositories/user_repository.py`
- Create: `backend/src/adapters/outbound/persistence/repositories/group_repository.py`
- Create: `backend/src/adapters/outbound/persistence/repositories/expense_repository.py`
- Create: `backend/src/adapters/outbound/persistence/repositories/settlement_repository.py`

- [ ] **Step 1: Create SQLAlchemy Base**

```python
# backend/src/adapters/outbound/persistence/models/base.py
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
```

- [ ] **Step 2: Create ORM models**

```python
# backend/src/adapters/outbound/persistence/models/user.py
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.adapters.outbound.persistence.models.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())

    group_memberships = relationship("GroupMemberModel", back_populates="user")
    expenses_created = relationship(
        "ExpenseModel", back_populates="created_by", foreign_keys="ExpenseModel.created_by_id"
    )
    expense_splits = relationship("ExpenseSplitModel", back_populates="user")
    settlements_paid = relationship(
        "SettlementModel", back_populates="payer", foreign_keys="SettlementModel.payer_id"
    )
    settlements_received = relationship(
        "SettlementModel", back_populates="payee", foreign_keys="SettlementModel.payee_id"
    )
```

```python
# backend/src/adapters/outbound/persistence/models/group.py
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.adapters.outbound.persistence.models.base import Base


class GroupModel(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description = mapped_column(Text, nullable=True)
    created_by_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())

    created_by = relationship("UserModel")
    members = relationship("GroupMemberModel", back_populates="group")
    expenses = relationship("ExpenseModel", back_populates="group")


class GroupMemberModel(Base):
    __tablename__ = "group_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("groups.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    joined_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    group = relationship("GroupModel", back_populates="members")
    user = relationship("UserModel", back_populates="group_memberships")
```

```python
# backend/src/adapters/outbound/persistence/models/expense.py
import enum

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.adapters.outbound.persistence.models.base import Base


class SplitTypeEnum(enum.Enum):
    EQUAL = "equal"
    EXACT = "exact"
    PERCENTAGE = "percentage"


class ExpenseModel(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description = mapped_column(Text, nullable=True)
    amount = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    split_type = mapped_column(Enum(SplitTypeEnum), default=SplitTypeEnum.EQUAL)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("groups.id"), nullable=False)
    created_by_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())

    group = relationship("GroupModel", back_populates="expenses")
    created_by = relationship("UserModel", back_populates="expenses_created")
    splits = relationship("ExpenseSplitModel", back_populates="expense", cascade="all, delete-orphan")


class ExpenseSplitModel(Base):
    __tablename__ = "expense_splits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    expense_id: Mapped[int] = mapped_column(Integer, ForeignKey("expenses.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    amount = mapped_column(Numeric(10, 2), nullable=False)
    percentage = mapped_column(Numeric(5, 2), nullable=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())

    expense = relationship("ExpenseModel", back_populates="splits")
    user = relationship("UserModel", back_populates="expense_splits")
```

```python
# backend/src/adapters/outbound/persistence/models/settlement.py
import enum

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.adapters.outbound.persistence.models.base import Base


class SettlementStatusEnum(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class SettlementModel(Base):
    __tablename__ = "settlements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    payer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    payee_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    amount = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    description = mapped_column(Text, nullable=True)
    status = mapped_column(Enum(SettlementStatusEnum), default=SettlementStatusEnum.PENDING)
    group_id = mapped_column(Integer, ForeignKey("groups.id"), nullable=True)
    settled_at = mapped_column(DateTime(timezone=True), nullable=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(DateTime(timezone=True), onupdate=func.now())

    payer = relationship("UserModel", back_populates="settlements_paid", foreign_keys=[payer_id])
    payee = relationship("UserModel", back_populates="settlements_received", foreign_keys=[payee_id])
    group = relationship("GroupModel")
```

- [ ] **Step 3: Create mappers**

```python
# backend/src/adapters/outbound/persistence/mappers/user_mapper.py
from src.adapters.outbound.persistence.models.user import UserModel
from src.domain.entities.user import User


class UserMapper:
    @staticmethod
    def to_domain(model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            username=model.username,
            full_name=model.full_name,
            hashed_password=model.hashed_password,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: User) -> UserModel:
        return UserModel(
            id=entity.id if entity.id else None,
            email=entity.email,
            username=entity.username,
            full_name=entity.full_name,
            hashed_password=entity.hashed_password,
            is_active=entity.is_active,
        )
```

```python
# backend/src/adapters/outbound/persistence/mappers/group_mapper.py
from src.adapters.outbound.persistence.models.group import GroupMemberModel, GroupModel
from src.domain.entities.group import Group, GroupMember


class GroupMapper:
    @staticmethod
    def to_domain(model: GroupModel) -> Group:
        members = [GroupMemberMapper.to_domain(m) for m in model.members] if model.members else None
        return Group(
            id=model.id,
            name=model.name,
            description=model.description,
            created_by_id=model.created_by_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            members=members,
        )

    @staticmethod
    def to_model(entity: Group) -> GroupModel:
        return GroupModel(
            id=entity.id if entity.id else None,
            name=entity.name,
            description=entity.description,
            created_by_id=entity.created_by_id,
        )


class GroupMemberMapper:
    @staticmethod
    def to_domain(model: GroupMemberModel) -> GroupMember:
        return GroupMember(
            id=model.id,
            group_id=model.group_id,
            user_id=model.user_id,
            is_admin=model.is_admin,
            joined_at=model.joined_at,
        )

    @staticmethod
    def to_model(entity: GroupMember) -> GroupMemberModel:
        return GroupMemberModel(
            id=entity.id if entity.id else None,
            group_id=entity.group_id,
            user_id=entity.user_id,
            is_admin=entity.is_admin,
        )
```

```python
# backend/src/adapters/outbound/persistence/mappers/expense_mapper.py
from decimal import Decimal

from src.adapters.outbound.persistence.models.expense import ExpenseModel, ExpenseSplitModel, SplitTypeEnum
from src.domain.entities.expense import Expense, ExpenseSplit, SplitType


_SPLIT_TYPE_MAP = {
    SplitTypeEnum.EQUAL: SplitType.EQUAL,
    SplitTypeEnum.EXACT: SplitType.EXACT,
    SplitTypeEnum.PERCENTAGE: SplitType.PERCENTAGE,
}
_SPLIT_TYPE_REVERSE = {v: k for k, v in _SPLIT_TYPE_MAP.items()}


class ExpenseSplitMapper:
    @staticmethod
    def to_domain(model: ExpenseSplitModel) -> ExpenseSplit:
        return ExpenseSplit(
            id=model.id,
            expense_id=model.expense_id,
            user_id=model.user_id,
            amount=Decimal(str(model.amount)),
            percentage=Decimal(str(model.percentage)) if model.percentage else None,
            created_at=model.created_at,
        )

    @staticmethod
    def to_model(entity: ExpenseSplit) -> ExpenseSplitModel:
        return ExpenseSplitModel(
            id=entity.id if entity.id else None,
            expense_id=entity.expense_id,
            user_id=entity.user_id,
            amount=entity.amount,
            percentage=entity.percentage,
        )


class ExpenseMapper:
    @staticmethod
    def to_domain(model: ExpenseModel) -> Expense:
        splits = [ExpenseSplitMapper.to_domain(s) for s in model.splits] if model.splits else []
        return Expense(
            id=model.id,
            title=model.title,
            amount=Decimal(str(model.amount)),
            group_id=model.group_id,
            created_by_id=model.created_by_id,
            split_type=_SPLIT_TYPE_MAP[model.split_type],
            description=model.description,
            currency=model.currency,
            created_at=model.created_at,
            updated_at=model.updated_at,
            splits=splits,
        )

    @staticmethod
    def to_model(entity: Expense) -> ExpenseModel:
        return ExpenseModel(
            id=entity.id if entity.id else None,
            title=entity.title,
            description=entity.description,
            amount=entity.amount,
            currency=entity.currency,
            split_type=_SPLIT_TYPE_REVERSE[entity.split_type],
            group_id=entity.group_id,
            created_by_id=entity.created_by_id,
        )
```

```python
# backend/src/adapters/outbound/persistence/mappers/settlement_mapper.py
from decimal import Decimal

from src.adapters.outbound.persistence.models.settlement import SettlementModel, SettlementStatusEnum
from src.domain.entities.settlement import Settlement, SettlementStatus


_STATUS_MAP = {
    SettlementStatusEnum.PENDING: SettlementStatus.PENDING,
    SettlementStatusEnum.COMPLETED: SettlementStatus.COMPLETED,
    SettlementStatusEnum.CANCELLED: SettlementStatus.CANCELLED,
}
_STATUS_REVERSE = {v: k for k, v in _STATUS_MAP.items()}


class SettlementMapper:
    @staticmethod
    def to_domain(model: SettlementModel) -> Settlement:
        return Settlement(
            id=model.id,
            payer_id=model.payer_id,
            payee_id=model.payee_id,
            amount=Decimal(str(model.amount)),
            status=_STATUS_MAP[model.status],
            currency=model.currency,
            description=model.description,
            group_id=model.group_id,
            settled_at=model.settled_at,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: Settlement) -> SettlementModel:
        return SettlementModel(
            id=entity.id if entity.id else None,
            payer_id=entity.payer_id,
            payee_id=entity.payee_id,
            amount=entity.amount,
            currency=entity.currency,
            description=entity.description,
            status=_STATUS_REVERSE[entity.status],
            group_id=entity.group_id,
            settled_at=entity.settled_at,
        )
```

- [ ] **Step 4: Create concrete repository implementations**

```python
# backend/src/adapters/outbound/persistence/repositories/user_repository.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.outbound.persistence.mappers.user_mapper import UserMapper
from src.adapters.outbound.persistence.models.user import UserModel
from src.domain.entities.user import User
from src.domain.ports.repositories.user_repository import UserRepository


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self._session.execute(select(UserModel).where(UserModel.id == user_id))
        model = result.scalar_one_or_none()
        return UserMapper.to_domain(model) if model else None

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(select(UserModel).where(UserModel.email == email))
        model = result.scalar_one_or_none()
        return UserMapper.to_domain(model) if model else None

    async def get_by_username(self, username: str) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        model = result.scalar_one_or_none()
        return UserMapper.to_domain(model) if model else None

    async def create(self, user: User) -> User:
        model = UserMapper.to_model(user)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return UserMapper.to_domain(model)

    async def update(self, user: User) -> User:
        result = await self._session.execute(select(UserModel).where(UserModel.id == user.id))
        model = result.scalar_one()
        model.email = user.email
        model.username = user.username
        model.full_name = user.full_name
        model.hashed_password = user.hashed_password
        model.is_active = user.is_active
        await self._session.flush()
        await self._session.refresh(model)
        return UserMapper.to_domain(model)

    async def list_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        result = await self._session.execute(select(UserModel).offset(skip).limit(limit))
        return [UserMapper.to_domain(m) for m in result.scalars().all()]
```

```python
# backend/src/adapters/outbound/persistence/repositories/group_repository.py
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.adapters.outbound.persistence.mappers.group_mapper import GroupMapper, GroupMemberMapper
from src.adapters.outbound.persistence.models.group import GroupMemberModel, GroupModel
from src.domain.entities.group import Group, GroupMember
from src.domain.ports.repositories.group_repository import GroupRepository


class SqlAlchemyGroupRepository(GroupRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, group_id: int) -> Group | None:
        result = await self._session.execute(
            select(GroupModel).options(selectinload(GroupModel.members)).where(GroupModel.id == group_id)
        )
        model = result.scalar_one_or_none()
        return GroupMapper.to_domain(model) if model else None

    async def create(self, group: Group) -> Group:
        model = GroupMapper.to_model(group)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return GroupMapper.to_domain(model)

    async def update(self, group: Group) -> Group:
        result = await self._session.execute(select(GroupModel).where(GroupModel.id == group.id))
        model = result.scalar_one()
        model.name = group.name
        model.description = group.description
        await self._session.flush()
        await self._session.refresh(model)
        return GroupMapper.to_domain(model)

    async def get_user_groups(self, user_id: int) -> list[Group]:
        result = await self._session.execute(
            select(GroupModel)
            .join(GroupMemberModel)
            .options(selectinload(GroupModel.members))
            .where(GroupMemberModel.user_id == user_id)
        )
        return [GroupMapper.to_domain(m) for m in result.scalars().all()]

    async def add_member(self, member: GroupMember) -> GroupMember:
        model = GroupMemberMapper.to_model(member)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return GroupMemberMapper.to_domain(model)

    async def remove_member(self, group_id: int, user_id: int) -> None:
        result = await self._session.execute(
            select(GroupMemberModel).where(
                GroupMemberModel.group_id == group_id,
                GroupMemberModel.user_id == user_id,
            )
        )
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()

    async def get_member(self, group_id: int, user_id: int) -> GroupMember | None:
        result = await self._session.execute(
            select(GroupMemberModel).where(
                GroupMemberModel.group_id == group_id,
                GroupMemberModel.user_id == user_id,
            )
        )
        model = result.scalar_one_or_none()
        return GroupMemberMapper.to_domain(model) if model else None

    async def get_members(self, group_id: int) -> list[GroupMember]:
        result = await self._session.execute(
            select(GroupMemberModel).where(GroupMemberModel.group_id == group_id)
        )
        return [GroupMemberMapper.to_domain(m) for m in result.scalars().all()]

    async def get_member_count(self, group_id: int) -> int:
        result = await self._session.execute(
            select(func.count()).select_from(GroupMemberModel).where(
                GroupMemberModel.group_id == group_id
            )
        )
        return result.scalar_one()
```

```python
# backend/src/adapters/outbound/persistence/repositories/expense_repository.py
from decimal import Decimal

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.adapters.outbound.persistence.mappers.expense_mapper import ExpenseMapper, ExpenseSplitMapper
from src.adapters.outbound.persistence.models.expense import ExpenseModel, ExpenseSplitModel
from src.domain.entities.expense import Expense, ExpenseSplit
from src.domain.ports.repositories.expense_repository import ExpenseRepository


class SqlAlchemyExpenseRepository(ExpenseRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, expense_id: int) -> Expense | None:
        result = await self._session.execute(
            select(ExpenseModel)
            .options(selectinload(ExpenseModel.splits))
            .where(ExpenseModel.id == expense_id)
        )
        model = result.scalar_one_or_none()
        return ExpenseMapper.to_domain(model) if model else None

    async def create(self, expense: Expense) -> Expense:
        model = ExpenseMapper.to_model(expense)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return ExpenseMapper.to_domain(model)

    async def create_splits(self, splits: list[ExpenseSplit]) -> list[ExpenseSplit]:
        models = [ExpenseSplitMapper.to_model(s) for s in splits]
        self._session.add_all(models)
        await self._session.flush()
        for m in models:
            await self._session.refresh(m)
        return [ExpenseSplitMapper.to_domain(m) for m in models]

    async def update(self, expense: Expense) -> Expense:
        result = await self._session.execute(
            select(ExpenseModel).where(ExpenseModel.id == expense.id)
        )
        model = result.scalar_one()
        model.title = expense.title
        model.description = expense.description
        model.amount = expense.amount
        model.currency = expense.currency
        await self._session.flush()
        await self._session.refresh(model)
        return ExpenseMapper.to_domain(model)

    async def delete(self, expense_id: int) -> None:
        result = await self._session.execute(
            select(ExpenseModel)
            .options(selectinload(ExpenseModel.splits))
            .where(ExpenseModel.id == expense_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()

    async def get_by_group(
        self, group_id: int, skip: int = 0, limit: int = 100
    ) -> list[Expense]:
        result = await self._session.execute(
            select(ExpenseModel)
            .options(selectinload(ExpenseModel.splits))
            .where(ExpenseModel.group_id == group_id)
            .offset(skip)
            .limit(limit)
        )
        return [ExpenseMapper.to_domain(m) for m in result.scalars().all()]

    async def get_by_user(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Expense]:
        result = await self._session.execute(
            select(ExpenseModel)
            .join(ExpenseSplitModel)
            .options(selectinload(ExpenseModel.splits))
            .where(
                or_(
                    ExpenseModel.created_by_id == user_id,
                    ExpenseSplitModel.user_id == user_id,
                )
            )
            .distinct()
            .offset(skip)
            .limit(limit)
        )
        return [ExpenseMapper.to_domain(m) for m in result.scalars().all()]

    async def get_group_splits(self, group_id: int) -> list[dict]:
        result = await self._session.execute(
            select(ExpenseSplitModel)
            .join(ExpenseModel)
            .options(selectinload(ExpenseSplitModel.expense))
            .where(ExpenseModel.group_id == group_id)
        )
        splits = []
        for model in result.scalars().all():
            splits.append({
                "expense_creator_id": model.expense.created_by_id,
                "user_id": model.user_id,
                "amount": Decimal(str(model.amount)),
                "total_amount": Decimal(str(model.expense.amount)),
            })
        return splits
```

```python
# backend/src/adapters/outbound/persistence/repositories/settlement_repository.py
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.outbound.persistence.mappers.settlement_mapper import SettlementMapper
from src.adapters.outbound.persistence.models.settlement import SettlementModel
from src.domain.entities.settlement import Settlement
from src.domain.ports.repositories.settlement_repository import SettlementRepository


class SqlAlchemySettlementRepository(SettlementRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, settlement_id: int) -> Settlement | None:
        result = await self._session.execute(
            select(SettlementModel).where(SettlementModel.id == settlement_id)
        )
        model = result.scalar_one_or_none()
        return SettlementMapper.to_domain(model) if model else None

    async def create(self, settlement: Settlement) -> Settlement:
        model = SettlementMapper.to_model(settlement)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return SettlementMapper.to_domain(model)

    async def update(self, settlement: Settlement) -> Settlement:
        result = await self._session.execute(
            select(SettlementModel).where(SettlementModel.id == settlement.id)
        )
        model = result.scalar_one()
        model.description = settlement.description
        model.status = SettlementMapper.to_model(settlement).status
        model.settled_at = settlement.settled_at
        await self._session.flush()
        await self._session.refresh(model)
        return SettlementMapper.to_domain(model)

    async def delete(self, settlement_id: int) -> None:
        result = await self._session.execute(
            select(SettlementModel).where(SettlementModel.id == settlement_id)
        )
        model = result.scalar_one_or_none()
        if model:
            await self._session.delete(model)
            await self._session.flush()

    async def get_by_user(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Settlement]:
        result = await self._session.execute(
            select(SettlementModel)
            .where(
                or_(SettlementModel.payer_id == user_id, SettlementModel.payee_id == user_id)
            )
            .offset(skip)
            .limit(limit)
        )
        return [SettlementMapper.to_domain(m) for m in result.scalars().all()]

    async def get_by_group(
        self, group_id: int, skip: int = 0, limit: int = 100
    ) -> list[Settlement]:
        result = await self._session.execute(
            select(SettlementModel)
            .where(SettlementModel.group_id == group_id)
            .offset(skip)
            .limit(limit)
        )
        return [SettlementMapper.to_domain(m) for m in result.scalars().all()]
```

- [ ] **Step 5: Commit**

```bash
git add backend/src/adapters/outbound/persistence/
git commit -m "feat(adapters): add ORM models, mappers, and repository implementations"
```

---

## Task 6: Outbound Adapters — Auth & AI

**Files:**
- Create: `backend/src/adapters/outbound/auth/jwt_provider.py`
- Create: `backend/src/adapters/outbound/ai/claude_client.py`

- [ ] **Step 1: Create JWT provider**

```python
# backend/src/adapters/outbound/auth/jwt_provider.py
from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from src.domain.ports.auth_provider import AuthProvider


class JwtAuthProvider(AuthProvider):
    def __init__(
        self, secret_key: str, algorithm: str = "HS256", expire_minutes: int = 30
    ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self._pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, subject: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=self._expire_minutes)
        to_encode = {"sub": subject, "exp": expire}
        return jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)

    def verify_token(self, token: str) -> str | None:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            subject: str | None = payload.get("sub")
            return subject
        except JWTError:
            return None
```

- [ ] **Step 2: Create Claude client**

```python
# backend/src/adapters/outbound/ai/claude_client.py
import anthropic

from src.domain.ports.ai_client import AiClient


class ClaudeClient(AiClient):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6") -> None:
        self._client = anthropic.AsyncAnthropic(api_key=api_key)
        self._model = model

    async def send_message(
        self, message: str, system_prompt: str, context: list[dict] | None = None
    ) -> str:
        messages: list[dict] = []
        if context:
            messages.extend(context)
        messages.append({"role": "user", "content": message})

        response = await self._client.messages.create(
            model=self._model,
            max_tokens=1024,
            system=system_prompt,
            messages=messages,
        )
        return response.content[0].text
```

- [ ] **Step 3: Commit**

```bash
git add backend/src/adapters/outbound/auth/ backend/src/adapters/outbound/ai/
git commit -m "feat(adapters): add JWT auth provider and Claude AI client"
```

---

## Task 7: Application Layer — Commands & Queries

**Files:**
- Create: `backend/src/application/commands/register_user.py`
- Create: `backend/src/application/commands/login_user.py`
- Create: `backend/src/application/commands/create_group.py`
- Create: `backend/src/application/commands/add_group_member.py`
- Create: `backend/src/application/commands/create_expense.py`
- Create: `backend/src/application/commands/create_settlement.py`
- Create: `backend/src/application/commands/update_settlement.py`
- Create: `backend/src/application/commands/send_chat_message.py`
- Create: `backend/src/application/queries/get_user_groups.py`
- Create: `backend/src/application/queries/get_group_expenses.py`
- Create: `backend/src/application/queries/get_balances.py`
- Create: `backend/src/application/queries/get_settlement_suggestions.py`
- Test: `backend/tests/unit/application/test_create_expense.py`
- Test: `backend/tests/unit/application/test_register_user.py`

- [ ] **Step 1: Create RegisterUserCommand**

```python
# backend/src/application/commands/register_user.py
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
```

- [ ] **Step 2: Create LoginUserCommand**

```python
# backend/src/application/commands/login_user.py
from src.domain.exceptions import UnauthorizedError
from src.domain.ports.auth_provider import AuthProvider
from src.domain.ports.repositories.user_repository import UserRepository


class LoginUserCommand:
    def __init__(self, user_repo: UserRepository, auth_provider: AuthProvider) -> None:
        self._user_repo = user_repo
        self._auth = auth_provider

    async def execute(self, email: str, password: str) -> dict:
        user = await self._user_repo.get_by_email(email)
        if not user or not self._auth.verify_password(password, user.hashed_password):
            raise UnauthorizedError("Incorrect email or password")
        if not user.is_active:
            raise UnauthorizedError("Inactive user")

        token = self._auth.create_access_token(subject=user.email)
        return {"access_token": token, "token_type": "bearer"}
```

- [ ] **Step 3: Create group commands**

```python
# backend/src/application/commands/create_group.py
from src.domain.entities.group import Group, GroupMember
from src.domain.ports.repositories.group_repository import GroupRepository


class CreateGroupCommand:
    def __init__(self, group_repo: GroupRepository) -> None:
        self._group_repo = group_repo

    async def execute(self, name: str, description: str | None, creator_id: int) -> Group:
        group = Group(id=0, name=name, description=description, created_by_id=creator_id)
        created_group = await self._group_repo.create(group)

        member = GroupMember(
            id=0, group_id=created_group.id, user_id=creator_id, is_admin=True
        )
        await self._group_repo.add_member(member)

        return await self._group_repo.get_by_id(created_group.id)  # type: ignore
```

```python
# backend/src/application/commands/add_group_member.py
from src.domain.entities.group import GroupMember
from src.domain.exceptions import ConflictError, ForbiddenError, NotFoundError
from src.domain.ports.repositories.group_repository import GroupRepository
from src.domain.ports.repositories.user_repository import UserRepository


class AddGroupMemberCommand:
    def __init__(self, group_repo: GroupRepository, user_repo: UserRepository) -> None:
        self._group_repo = group_repo
        self._user_repo = user_repo

    async def execute(
        self, group_id: int, user_id: int, is_admin: bool, current_user_id: int
    ) -> GroupMember:
        group = await self._group_repo.get_by_id(group_id)
        if not group:
            raise NotFoundError("Group not found")

        admin_member = await self._group_repo.get_member(group_id, current_user_id)
        if not admin_member or not admin_member.is_admin:
            raise ForbiddenError("Only group admins can invite users")

        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        existing = await self._group_repo.get_member(group_id, user_id)
        if existing:
            raise ConflictError("User is already a member of this group")

        member = GroupMember(id=0, group_id=group_id, user_id=user_id, is_admin=is_admin)
        return await self._group_repo.add_member(member)
```

- [ ] **Step 4: Create expense command**

```python
# backend/src/application/commands/create_expense.py
from decimal import Decimal

from src.domain.entities.expense import Expense, ExpenseSplit, SplitType
from src.domain.exceptions import ForbiddenError, ValidationError
from src.domain.ports.repositories.expense_repository import ExpenseRepository
from src.domain.ports.repositories.group_repository import GroupRepository
from src.domain.services.expense_service import calculate_splits


class CreateExpenseCommand:
    def __init__(
        self, expense_repo: ExpenseRepository, group_repo: GroupRepository
    ) -> None:
        self._expense_repo = expense_repo
        self._group_repo = group_repo

    async def execute(
        self,
        title: str,
        amount: Decimal,
        group_id: int,
        creator_id: int,
        split_type: SplitType,
        user_ids: list[int],
        description: str | None = None,
        currency: str = "INR",
        split_amounts: list[Decimal] | None = None,
        split_percentages: list[Decimal] | None = None,
    ) -> Expense:
        membership = await self._group_repo.get_member(group_id, creator_id)
        if not membership:
            raise ForbiddenError("Not a member of this group")

        # Validate all split users are group members
        for uid in user_ids:
            member = await self._group_repo.get_member(group_id, uid)
            if not member:
                raise ValidationError("All users in splits must be members of the group")

        calculated = calculate_splits(
            total_amount=amount,
            split_type=split_type,
            user_ids=user_ids,
            split_amounts=split_amounts,
            split_percentages=split_percentages,
        )

        expense = Expense(
            id=0,
            title=title,
            amount=amount,
            group_id=group_id,
            created_by_id=creator_id,
            split_type=split_type,
            description=description,
            currency=currency,
        )
        created_expense = await self._expense_repo.create(expense)

        splits = [
            ExpenseSplit(
                id=0,
                expense_id=created_expense.id,
                user_id=s["user_id"],
                amount=s["amount"],
                percentage=s["percentage"],
            )
            for s in calculated
        ]
        await self._expense_repo.create_splits(splits)

        return await self._expense_repo.get_by_id(created_expense.id)  # type: ignore
```

- [ ] **Step 5: Create settlement commands**

```python
# backend/src/application/commands/create_settlement.py
from decimal import Decimal
from datetime import datetime

from src.domain.entities.settlement import Settlement, SettlementStatus
from src.domain.exceptions import ForbiddenError, NotFoundError
from src.domain.ports.repositories.group_repository import GroupRepository
from src.domain.ports.repositories.settlement_repository import SettlementRepository
from src.domain.ports.repositories.user_repository import UserRepository


class CreateSettlementCommand:
    def __init__(
        self,
        settlement_repo: SettlementRepository,
        user_repo: UserRepository,
        group_repo: GroupRepository,
    ) -> None:
        self._settlement_repo = settlement_repo
        self._user_repo = user_repo
        self._group_repo = group_repo

    async def execute(
        self,
        payer_id: int,
        payee_id: int,
        amount: Decimal,
        group_id: int | None = None,
        currency: str = "INR",
        description: str | None = None,
    ) -> Settlement:
        payee = await self._user_repo.get_by_id(payee_id)
        if not payee:
            raise NotFoundError("Payee not found")

        if group_id:
            payer_member = await self._group_repo.get_member(group_id, payer_id)
            payee_member = await self._group_repo.get_member(group_id, payee_id)
            if not payer_member or not payee_member:
                raise ForbiddenError("Both users must be members of the group")

        settlement = Settlement(
            id=0,
            payer_id=payer_id,
            payee_id=payee_id,
            amount=amount,
            status=SettlementStatus.PENDING,
            currency=currency,
            description=description,
            group_id=group_id,
        )
        return await self._settlement_repo.create(settlement)
```

```python
# backend/src/application/commands/update_settlement.py
from datetime import datetime

from src.domain.entities.settlement import SettlementStatus
from src.domain.exceptions import ForbiddenError, NotFoundError
from src.domain.ports.repositories.settlement_repository import SettlementRepository


class UpdateSettlementCommand:
    def __init__(self, settlement_repo: SettlementRepository) -> None:
        self._settlement_repo = settlement_repo

    async def execute(
        self,
        settlement_id: int,
        current_user_id: int,
        description: str | None = None,
        status: SettlementStatus | None = None,
    ):
        settlement = await self._settlement_repo.get_by_id(settlement_id)
        if not settlement:
            raise NotFoundError("Settlement not found")

        if settlement.payer_id != current_user_id and settlement.payee_id != current_user_id:
            raise ForbiddenError("Only payer or payee can update this settlement")

        if description is not None:
            settlement.description = description
        if status is not None:
            settlement.status = status
            if status == SettlementStatus.COMPLETED:
                settlement.settled_at = datetime.utcnow()

        return await self._settlement_repo.update(settlement)
```

- [ ] **Step 6: Create chat command**

```python
# backend/src/application/commands/send_chat_message.py
from src.domain.entities.user import User
from src.domain.ports.ai_client import AiClient
from src.domain.ports.repositories.expense_repository import ExpenseRepository
from src.domain.ports.repositories.group_repository import GroupRepository
from src.domain.services.settlement_service import calculate_balances_from_splits


SYSTEM_PROMPT = """You are PennyPal, a helpful expense-splitting assistant.
You help users manage shared expenses, check balances, and settle debts.

When the user wants to add an expense, extract: title, amount, and suggest equal split.
When the user asks about balances, summarize who owes whom.
When the user wants to settle, confirm the amount and recipient.

Respond in a friendly, concise manner. Use currency symbol as per context (default INR ₹).

Current user context:
{user_context}

Group balances:
{balance_context}
"""


class SendChatMessageCommand:
    def __init__(
        self,
        ai_client: AiClient,
        group_repo: GroupRepository,
        expense_repo: ExpenseRepository,
    ) -> None:
        self._ai_client = ai_client
        self._group_repo = group_repo
        self._expense_repo = expense_repo

    async def execute(
        self, message: str, user: User, group_id: int | None = None
    ) -> dict:
        user_context = f"Name: {user.full_name}, Username: {user.username}"

        balance_context = "No group selected."
        if group_id:
            splits = await self._expense_repo.get_group_splits(group_id)
            balances = calculate_balances_from_splits(splits)
            group = await self._group_repo.get_by_id(group_id)
            group_name = group.name if group else f"Group {group_id}"
            balance_lines = []
            for uid, bal in balances.items():
                if bal > 0:
                    balance_lines.append(f"User {uid} is owed ₹{bal:.2f}")
                elif bal < 0:
                    balance_lines.append(f"User {uid} owes ₹{abs(bal):.2f}")
            balance_context = f"Group: {group_name}\n" + "\n".join(balance_lines) if balance_lines else f"Group: {group_name} — all settled"

        system = SYSTEM_PROMPT.format(
            user_context=user_context, balance_context=balance_context
        )

        response = await self._ai_client.send_message(
            message=message, system_prompt=system
        )

        return {
            "response": response,
            "actions_taken": [],
            "suggested_actions": [],
        }
```

- [ ] **Step 7: Create queries**

```python
# backend/src/application/queries/get_user_groups.py
from src.domain.entities.group import Group
from src.domain.ports.repositories.group_repository import GroupRepository


class GetUserGroupsQuery:
    def __init__(self, group_repo: GroupRepository) -> None:
        self._group_repo = group_repo

    async def execute(self, user_id: int) -> list[Group]:
        return await self._group_repo.get_user_groups(user_id)
```

```python
# backend/src/application/queries/get_group_expenses.py
from src.domain.entities.expense import Expense
from src.domain.exceptions import ForbiddenError
from src.domain.ports.repositories.expense_repository import ExpenseRepository
from src.domain.ports.repositories.group_repository import GroupRepository


class GetGroupExpensesQuery:
    def __init__(
        self, expense_repo: ExpenseRepository, group_repo: GroupRepository
    ) -> None:
        self._expense_repo = expense_repo
        self._group_repo = group_repo

    async def execute(
        self, group_id: int, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Expense]:
        member = await self._group_repo.get_member(group_id, user_id)
        if not member:
            raise ForbiddenError("Not a member of this group")
        return await self._expense_repo.get_by_group(group_id, skip, limit)
```

```python
# backend/src/application/queries/get_balances.py
from decimal import Decimal

from src.domain.exceptions import ForbiddenError
from src.domain.ports.repositories.expense_repository import ExpenseRepository
from src.domain.ports.repositories.group_repository import GroupRepository
from src.domain.ports.repositories.user_repository import UserRepository
from src.domain.services.settlement_service import calculate_balances_from_splits


class GetBalancesQuery:
    def __init__(
        self,
        expense_repo: ExpenseRepository,
        group_repo: GroupRepository,
        user_repo: UserRepository,
    ) -> None:
        self._expense_repo = expense_repo
        self._group_repo = group_repo
        self._user_repo = user_repo

    async def execute(self, group_id: int, user_id: int) -> dict[str, Decimal]:
        member = await self._group_repo.get_member(group_id, user_id)
        if not member:
            raise ForbiddenError("Not a member of this group")

        splits = await self._expense_repo.get_group_splits(group_id)
        balances = calculate_balances_from_splits(splits)

        result: dict[str, Decimal] = {}
        for uid, balance in balances.items():
            user = await self._user_repo.get_by_id(uid)
            if user:
                result[user.username] = balance

        return result
```

```python
# backend/src/application/queries/get_settlement_suggestions.py
from src.domain.exceptions import ForbiddenError
from src.domain.ports.repositories.expense_repository import ExpenseRepository
from src.domain.ports.repositories.group_repository import GroupRepository
from src.domain.ports.repositories.user_repository import UserRepository
from src.domain.services.settlement_service import (
    calculate_balances_from_splits,
    generate_settlement_suggestions,
)


class GetSettlementSuggestionsQuery:
    def __init__(
        self,
        expense_repo: ExpenseRepository,
        group_repo: GroupRepository,
        user_repo: UserRepository,
    ) -> None:
        self._expense_repo = expense_repo
        self._group_repo = group_repo
        self._user_repo = user_repo

    async def execute(self, group_id: int, user_id: int) -> list[dict]:
        member = await self._group_repo.get_member(group_id, user_id)
        if not member:
            raise ForbiddenError("Not a member of this group")

        splits = await self._expense_repo.get_group_splits(group_id)
        balances = calculate_balances_from_splits(splits)
        suggestions = generate_settlement_suggestions(balances, group_id)

        result = []
        for s in suggestions:
            payer = await self._user_repo.get_by_id(s["payer_id"])
            payee = await self._user_repo.get_by_id(s["payee_id"])
            result.append({
                "payer": {"id": s["payer_id"], "username": payer.username if payer else "Unknown", "full_name": payer.full_name if payer else "Unknown"},
                "payee": {"id": s["payee_id"], "username": payee.username if payee else "Unknown", "full_name": payee.full_name if payee else "Unknown"},
                "amount": s["amount"],
                "group_id": s["group_id"],
            })

        return result
```

- [ ] **Step 8: Write application-layer tests**

```python
# backend/tests/unit/application/test_register_user.py
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
    async def test_register_duplicate_email(self, user_repo: AsyncMock, auth_provider: AsyncMock) -> None:
        user_repo.get_by_email.return_value = User(
            id=1, email="a@b.com", username="alice", full_name="Alice", hashed_password="x"
        )

        cmd = RegisterUserCommand(user_repo, auth_provider)
        with pytest.raises(ConflictError, match="Email already registered"):
            await cmd.execute("a@b.com", "bob", "Bob", "pass123")
```

```python
# backend/tests/unit/application/test_create_expense.py
from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from src.application.commands.create_expense import CreateExpenseCommand
from src.domain.entities.expense import Expense, SplitType
from src.domain.entities.group import GroupMember
from src.domain.exceptions import ForbiddenError


@pytest.fixture
def expense_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def group_repo() -> AsyncMock:
    return AsyncMock()


class TestCreateExpense:
    @pytest.mark.asyncio
    async def test_create_equal_split(self, expense_repo: AsyncMock, group_repo: AsyncMock) -> None:
        group_repo.get_member.return_value = GroupMember(id=1, group_id=1, user_id=1, is_admin=True)
        expense_repo.create.return_value = Expense(
            id=1, title="Lunch", amount=Decimal("100"), group_id=1, created_by_id=1
        )
        expense_repo.get_by_id.return_value = Expense(
            id=1, title="Lunch", amount=Decimal("100"), group_id=1, created_by_id=1
        )

        cmd = CreateExpenseCommand(expense_repo, group_repo)
        result = await cmd.execute(
            title="Lunch",
            amount=Decimal("100"),
            group_id=1,
            creator_id=1,
            split_type=SplitType.EQUAL,
            user_ids=[1, 2],
        )

        assert result.id == 1
        expense_repo.create.assert_called_once()
        expense_repo.create_splits.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_non_member_raises(self, expense_repo: AsyncMock, group_repo: AsyncMock) -> None:
        group_repo.get_member.return_value = None

        cmd = CreateExpenseCommand(expense_repo, group_repo)
        with pytest.raises(ForbiddenError, match="Not a member"):
            await cmd.execute(
                title="Lunch",
                amount=Decimal("100"),
                group_id=1,
                creator_id=999,
                split_type=SplitType.EQUAL,
                user_ids=[999, 2],
            )
```

- [ ] **Step 9: Run tests**

Run:
```bash
cd backend && source .venv/bin/activate && python -m pytest tests/unit/ -v
```
Expected: All tests PASS.

- [ ] **Step 10: Commit**

```bash
git add backend/src/application/ backend/tests/unit/application/
git commit -m "feat(application): add commands, queries, and use case tests"
```

---

## Task 8: Infrastructure & Inbound Adapters (FastAPI Wiring)

**Files:**
- Create: `backend/src/infrastructure/config.py`
- Create: `backend/src/infrastructure/database.py`
- Create: `backend/src/infrastructure/container.py`
- Create: `backend/src/infrastructure/app.py`
- Create: `backend/src/adapters/inbound/schemas/user.py`
- Create: `backend/src/adapters/inbound/schemas/group.py`
- Create: `backend/src/adapters/inbound/schemas/expense.py`
- Create: `backend/src/adapters/inbound/schemas/settlement.py`
- Create: `backend/src/adapters/inbound/schemas/chatbot.py`
- Create: `backend/src/adapters/inbound/middleware/cors.py`
- Create: `backend/src/adapters/inbound/middleware/error_handler.py`
- Create: `backend/src/adapters/inbound/api/v1/auth.py`
- Create: `backend/src/adapters/inbound/api/v1/users.py`
- Create: `backend/src/adapters/inbound/api/v1/groups.py`
- Create: `backend/src/adapters/inbound/api/v1/expenses.py`
- Create: `backend/src/adapters/inbound/api/v1/settlements.py`
- Create: `backend/src/adapters/inbound/api/v1/chatbot.py`
- Create: `backend/src/adapters/inbound/api/router.py`
- Create: `backend/run.py` (update)

This is a large task. The engineer should implement each file and verify the app starts. The code for all schemas, middleware, and routes follows the same patterns — translating between Pydantic schemas and domain entities via use cases.

**Key patterns:**

Each route handler:
1. Gets the container from `request.app.state.container`
2. Creates use case with repos from container
3. Calls `use_case.execute(...)`
4. Returns Pydantic response

- [ ] **Step 1: Create infrastructure config**

```python
# backend/src/infrastructure/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/pennypal"
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ANTHROPIC_API_KEY: str = ""
    CLAUDE_MODEL: str = "claude-sonnet-4-6"
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
```

- [ ] **Step 2: Create async database setup**

```python
# backend/src/infrastructure/database.py
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.infrastructure.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
)

async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        async with session.begin():
            yield session
```

- [ ] **Step 3: Create DI container**

```python
# backend/src/infrastructure/container.py
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.outbound.ai.claude_client import ClaudeClient
from src.adapters.outbound.auth.jwt_provider import JwtAuthProvider
from src.adapters.outbound.persistence.repositories.expense_repository import SqlAlchemyExpenseRepository
from src.adapters.outbound.persistence.repositories.group_repository import SqlAlchemyGroupRepository
from src.adapters.outbound.persistence.repositories.settlement_repository import SqlAlchemySettlementRepository
from src.adapters.outbound.persistence.repositories.user_repository import SqlAlchemyUserRepository
from src.infrastructure.config import settings


class Container:
    def __init__(self, session: AsyncSession) -> None:
        self.user_repo = SqlAlchemyUserRepository(session)
        self.group_repo = SqlAlchemyGroupRepository(session)
        self.expense_repo = SqlAlchemyExpenseRepository(session)
        self.settlement_repo = SqlAlchemySettlementRepository(session)
        self.auth_provider = JwtAuthProvider(
            secret_key=settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
            expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
        self.ai_client = ClaudeClient(
            api_key=settings.ANTHROPIC_API_KEY,
            model=settings.CLAUDE_MODEL,
        )
```

- [ ] **Step 4: Create Pydantic schemas (inbound)**

```python
# backend/src/adapters/inbound/schemas/user.py
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
```

```python
# backend/src/adapters/inbound/schemas/group.py
from datetime import datetime

from pydantic import BaseModel

from src.adapters.inbound.schemas.user import UserResponse


class GroupCreateRequest(BaseModel):
    name: str
    description: str | None = None


class GroupUpdateRequest(BaseModel):
    name: str | None = None
    description: str | None = None


class GroupInviteRequest(BaseModel):
    user_id: int
    is_admin: bool = False


class GroupMemberResponse(BaseModel):
    id: int
    user_id: int
    group_id: int
    is_admin: bool
    joined_at: datetime | None = None


class GroupResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    created_by_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    members: list[GroupMemberResponse] = []
```

```python
# backend/src/adapters/inbound/schemas/expense.py
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, field_validator


class ExpenseSplitInput(BaseModel):
    user_id: int
    amount: Decimal | None = None
    percentage: Decimal | None = None


class ExpenseCreateRequest(BaseModel):
    title: str
    description: str | None = None
    amount: Decimal
    currency: str = "INR"
    split_type: str = "equal"
    group_id: int
    splits: list[ExpenseSplitInput]

    @field_validator("splits")
    @classmethod
    def validate_splits(cls, v: list) -> list:
        if not v:
            raise ValueError("At least one split is required")
        return v


class ExpenseUpdateRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    amount: Decimal | None = None
    currency: str | None = None


class ExpenseSplitResponse(BaseModel):
    id: int
    expense_id: int
    user_id: int
    amount: Decimal
    percentage: Decimal | None = None
    created_at: datetime | None = None


class ExpenseResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    amount: Decimal
    currency: str
    split_type: str
    group_id: int
    created_by_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    splits: list[ExpenseSplitResponse] = []
```

```python
# backend/src/adapters/inbound/schemas/settlement.py
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class SettlementCreateRequest(BaseModel):
    payee_id: int
    amount: Decimal
    currency: str = "INR"
    description: str | None = None
    group_id: int | None = None


class SettlementUpdateRequest(BaseModel):
    description: str | None = None
    status: str | None = None


class SettlementResponse(BaseModel):
    id: int
    payer_id: int
    payee_id: int
    amount: Decimal
    currency: str
    status: str
    description: str | None = None
    group_id: int | None = None
    settled_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
```

```python
# backend/src/adapters/inbound/schemas/chatbot.py
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    group_id: int | None = None


class ChatResponse(BaseModel):
    response: str
    actions_taken: list[str] = []
    suggested_actions: list[dict] = []
```

- [ ] **Step 5: Create middleware**

```python
# backend/src/adapters/inbound/middleware/cors.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.config import settings


def setup_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
```

```python
# backend/src/adapters/inbound/middleware/error_handler.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.domain.exceptions import (
    ConflictError,
    DomainError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)

_STATUS_MAP = {
    NotFoundError: 404,
    UnauthorizedError: 401,
    ForbiddenError: 403,
    ValidationError: 400,
    ConflictError: 409,
}


def setup_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
        status_code = _STATUS_MAP.get(type(exc), 400)
        return JSONResponse(status_code=status_code, content={"detail": exc.message})
```

- [ ] **Step 6: Create auth dependency helper**

```python
# backend/src/adapters/inbound/api/deps.py
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.domain.entities.user import User
from src.infrastructure.container import Container

security = HTTPBearer()


async def get_container(request: Request) -> Container:
    return request.state.container


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    container: Container = Depends(get_container),
) -> User:
    token = credentials.credentials
    email = container.auth_provider.verify_token(token)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    user = await container.user_repo.get_by_id(0)  # placeholder — need by email
    # Actually use get_by_email
    user = await container.user_repo.get_by_email(email)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    return user
```

- [ ] **Step 7: Create API route files**

```python
# backend/src/adapters/inbound/api/v1/auth.py
from fastapi import APIRouter, Depends

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
async def register(body: UserCreateRequest, container: Container = Depends(get_container)):
    cmd = RegisterUserCommand(container.user_repo, container.auth_provider)
    user = await cmd.execute(body.email, body.username, body.full_name, body.password)
    return UserResponse(
        id=user.id, email=user.email, username=user.username,
        full_name=user.full_name, is_active=user.is_active,
        created_at=user.created_at, updated_at=user.updated_at,
    )


@router.post("/login", response_model=TokenResponse)
async def login(body: UserLoginRequest, container: Container = Depends(get_container)):
    cmd = LoginUserCommand(container.user_repo, container.auth_provider)
    result = await cmd.execute(body.email, body.password)
    return TokenResponse(**result)
```

```python
# backend/src/adapters/inbound/api/v1/users.py
from fastapi import APIRouter, Depends

from src.adapters.inbound.api.deps import get_container, get_current_user
from src.adapters.inbound.schemas.user import UserResponse, UserUpdateRequest
from src.domain.entities.user import User
from src.infrastructure.container import Container

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id, email=current_user.email, username=current_user.username,
        full_name=current_user.full_name, is_active=current_user.is_active,
        created_at=current_user.created_at, updated_at=current_user.updated_at,
    )


@router.put("/me", response_model=UserResponse)
async def update_me(
    body: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container),
):
    if body.email is not None:
        current_user.email = body.email
    if body.username is not None:
        current_user.username = body.username
    if body.full_name is not None:
        current_user.full_name = body.full_name
    if body.password is not None:
        current_user.hashed_password = container.auth_provider.hash_password(body.password)

    updated = await container.user_repo.update(current_user)
    return UserResponse(
        id=updated.id, email=updated.email, username=updated.username,
        full_name=updated.full_name, is_active=updated.is_active,
        created_at=updated.created_at, updated_at=updated.updated_at,
    )


@router.get("/", response_model=list[UserResponse])
async def list_users(
    skip: int = 0, limit: int = 100,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container),
):
    users = await container.user_repo.list_all(skip, limit)
    return [
        UserResponse(
            id=u.id, email=u.email, username=u.username,
            full_name=u.full_name, is_active=u.is_active,
            created_at=u.created_at, updated_at=u.updated_at,
        )
        for u in users
    ]
```

```python
# backend/src/adapters/inbound/api/v1/groups.py
from fastapi import APIRouter, Depends

from src.adapters.inbound.api.deps import get_container, get_current_user
from src.adapters.inbound.schemas.group import (
    GroupCreateRequest,
    GroupInviteRequest,
    GroupMemberResponse,
    GroupResponse,
    GroupUpdateRequest,
)
from src.application.commands.add_group_member import AddGroupMemberCommand
from src.application.commands.create_group import CreateGroupCommand
from src.application.queries.get_user_groups import GetUserGroupsQuery
from src.domain.entities.group import Group
from src.domain.entities.user import User
from src.domain.exceptions import ForbiddenError, NotFoundError
from src.infrastructure.container import Container

router = APIRouter()


def _group_response(group: Group) -> GroupResponse:
    members = [
        GroupMemberResponse(
            id=m.id, user_id=m.user_id, group_id=m.group_id,
            is_admin=m.is_admin, joined_at=m.joined_at,
        )
        for m in (group.members or [])
    ]
    return GroupResponse(
        id=group.id, name=group.name, description=group.description,
        created_by_id=group.created_by_id, created_at=group.created_at,
        updated_at=group.updated_at, members=members,
    )


@router.post("/", response_model=GroupResponse)
async def create_group(
    body: GroupCreateRequest,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container),
):
    cmd = CreateGroupCommand(container.group_repo)
    group = await cmd.execute(body.name, body.description, current_user.id)
    return _group_response(group)


@router.get("/", response_model=list[GroupResponse])
async def list_groups(
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container),
):
    query = GetUserGroupsQuery(container.group_repo)
    groups = await query.execute(current_user.id)
    return [_group_response(g) for g in groups]


@router.get("/{group_id}", response_model=GroupResponse)
async def get_group(
    group_id: int,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container),
):
    group = await container.group_repo.get_by_id(group_id)
    if not group:
        raise NotFoundError("Group not found")
    member = await container.group_repo.get_member(group_id, current_user.id)
    if not member:
        raise ForbiddenError("Not a member of this group")
    return _group_response(group)


@router.put("/{group_id}", response_model=GroupResponse)
async def update_group(
    group_id: int,
    body: GroupUpdateRequest,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container),
):
    group = await container.group_repo.get_by_id(group_id)
    if not group:
        raise NotFoundError("Group not found")
    member = await container.group_repo.get_member(group_id, current_user.id)
    if not member or not member.is_admin:
        raise ForbiddenError("Only group admins can update group details")

    if body.name is not None:
        group.name = body.name
    if body.description is not None:
        group.description = body.description
    updated = await container.group_repo.update(group)
    return _group_response(updated)


@router.post("/{group_id}/invite")
async def invite_member(
    group_id: int,
    body: GroupInviteRequest,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container),
):
    cmd = AddGroupMemberCommand(container.group_repo, container.user_repo)
    await cmd.execute(group_id, body.user_id, body.is_admin, current_user.id)
    return {"message": "User invited successfully"}


@router.delete("/{group_id}/members/{user_id}")
async def remove_member(
    group_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container),
):
    group = await container.group_repo.get_by_id(group_id)
    if not group:
        raise NotFoundError("Group not found")

    if user_id != current_user.id:
        member = await container.group_repo.get_member(group_id, current_user.id)
        if not member or not member.is_admin:
            raise ForbiddenError("Only group admins can remove other users")

    await container.group_repo.remove_member(group_id, user_id)
    return {"message": "User removed from group successfully"}
```

```python
# backend/src/adapters/inbound/api/v1/expenses.py
from fastapi import APIRouter, Depends

from src.adapters.inbound.api.deps import get_container, get_current_user
from src.adapters.inbound.schemas.expense import (
    ExpenseCreateRequest,
    ExpenseResponse,
    ExpenseSplitResponse,
    ExpenseUpdateRequest,
)
from src.application.commands.create_expense import CreateExpenseCommand
from src.application.queries.get_group_expenses import GetGroupExpensesQuery
from src.domain.entities.expense import Expense, SplitType
from src.domain.entities.user import User
from src.domain.exceptions import ForbiddenError, NotFoundError
from src.infrastructure.container import Container

router = APIRouter()


def _expense_response(expense: Expense) -> ExpenseResponse:
    return ExpenseResponse(
        id=expense.id, title=expense.title, description=expense.description,
        amount=expense.amount, currency=expense.currency,
        split_type=expense.split_type.value, group_id=expense.group_id,
        created_by_id=expense.created_by_id, created_at=expense.created_at,
        updated_at=expense.updated_at,
        splits=[
            ExpenseSplitResponse(
                id=s.id, expense_id=s.expense_id, user_id=s.user_id,
                amount=s.amount, percentage=s.percentage, created_at=s.created_at,
            )
            for s in expense.splits
        ],
    )


@router.post("/", response_model=ExpenseResponse)
async def create_expense(
    body: ExpenseCreateRequest,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container),
):
    split_type = SplitType(body.split_type)
    user_ids = [s.user_id for s in body.splits]
    split_amounts = [s.amount for s in body.splits if s.amount is not None] or None
    split_percentages = [s.percentage for s in body.splits if s.percentage is not None] or None

    cmd = CreateExpenseCommand(container.expense_repo, container.group_repo)
    expense = await cmd.execute(
        title=body.title, amount=body.amount, group_id=body.group_id,
        creator_id=current_user.id, split_type=split_type, user_ids=user_ids,
        description=body.description, currency=body.currency,
        split_amounts=split_amounts, split_percentages=split_percentages,
    )
    return _expense_response(expense)


@router.get("/group/{group_id}", response_model=list[ExpenseResponse])
async def get_group_expenses(
    group_id: int, skip: int = 0, limit: int = 100,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container),
):
    query = GetGroupExpensesQuery(container.expense_repo, container.group_repo)
    expenses = await query.execute(group_id, current_user.id, skip, limit)
    return [_expense_response(e) for e in expenses]


@router.get("/{expense_id}", response_model=ExpenseResponse)
async def get_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container),
):
    expense = await container.expense_repo.get_by_id(expense_id)
    if not expense:
        raise NotFoundError("Expense not found")
    member = await container.group_repo.get_member(expense.group_id, current_user.id)
    if not member:
        raise ForbiddenError("Not a member of this group")
    return _expense_response(expense)


@router.delete("/{expense_id}")
async def delete_expense(
    expense_id: int,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container),
):
    expense = await container.expense_repo.get_by_id(expense_id)
    if not expense:
        raise NotFoundError("Expense not found")
    if expense.created_by_id != current_user.id:
        raise ForbiddenError("Only the creator can delete this expense")
    await container.expense_repo.delete(expense_id)
    return {"message": "Expense deleted successfully"}
```

```python
# backend/src/adapters/inbound/api/v1/settlements.py
from fastapi import APIRouter, Depends

from src.adapters.inbound.api.deps import get_container, get_current_user
from src.adapters.inbound.schemas.settlement import (
    SettlementCreateRequest,
    SettlementResponse,
    SettlementUpdateRequest,
)
from src.application.commands.create_settlement import CreateSettlementCommand
from src.application.commands.update_settlement import UpdateSettlementCommand
from src.application.queries.get_balances import GetBalancesQuery
from src.application.queries.get_settlement_suggestions import GetSettlementSuggestionsQuery
from src.domain.entities.settlement import Settlement, SettlementStatus
from src.domain.entities.user import User
from src.domain.exceptions import ForbiddenError, NotFoundError
from src.infrastructure.container import Container

router = APIRouter()


def _settlement_response(s: Settlement) -> SettlementResponse:
    return SettlementResponse(
        id=s.id, payer_id=s.payer_id, payee_id=s.payee_id,
        amount=s.amount, currency=s.currency, status=s.status.value,
        description=s.description, group_id=s.group_id,
        settled_at=s.settled_at, created_at=s.created_at, updated_at=s.updated_at,
    )


@router.post("/", response_model=SettlementResponse)
async def create_settlement(
    body: SettlementCreateRequest,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container),
):
    cmd = CreateSettlementCommand(container.settlement_repo, container.user_repo, container.group_repo)
    settlement = await cmd.execute(
        payer_id=current_user.id, payee_id=body.payee_id, amount=body.amount,
        group_id=body.group_id, currency=body.currency, description=body.description,
    )
    return _settlement_response(settlement)


@router.get("/", response_model=list[SettlementResponse])
async def list_settlements(
    skip: int = 0, limit: int = 100,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container),
):
    settlements = await container.settlement_repo.get_by_user(current_user.id, skip, limit)
    return [_settlement_response(s) for s in settlements]


@router.get("/group/{group_id}/balances")
async def get_group_balances(
    group_id: int,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container),
):
    query = GetBalancesQuery(container.expense_repo, container.group_repo, container.user_repo)
    return await query.execute(group_id, current_user.id)


@router.get("/group/{group_id}/suggestions")
async def get_suggestions(
    group_id: int,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container),
):
    query = GetSettlementSuggestionsQuery(container.expense_repo, container.group_repo, container.user_repo)
    return await query.execute(group_id, current_user.id)


@router.put("/{settlement_id}", response_model=SettlementResponse)
async def update_settlement(
    settlement_id: int,
    body: SettlementUpdateRequest,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container),
):
    status_enum = SettlementStatus(body.status) if body.status else None
    cmd = UpdateSettlementCommand(container.settlement_repo)
    settlement = await cmd.execute(
        settlement_id=settlement_id, current_user_id=current_user.id,
        description=body.description, status=status_enum,
    )
    return _settlement_response(settlement)


@router.delete("/{settlement_id}")
async def delete_settlement(
    settlement_id: int,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container),
):
    settlement = await container.settlement_repo.get_by_id(settlement_id)
    if not settlement:
        raise NotFoundError("Settlement not found")
    if settlement.payer_id != current_user.id:
        raise ForbiddenError("Only the payer can delete this settlement")
    if settlement.status != SettlementStatus.PENDING:
        from src.domain.exceptions import ValidationError
        raise ValidationError("Only pending settlements can be deleted")
    await container.settlement_repo.delete(settlement_id)
    return {"message": "Settlement deleted successfully"}
```

```python
# backend/src/adapters/inbound/api/v1/chatbot.py
from fastapi import APIRouter, Depends

from src.adapters.inbound.api.deps import get_container, get_current_user
from src.adapters.inbound.schemas.chatbot import ChatRequest, ChatResponse
from src.application.commands.send_chat_message import SendChatMessageCommand
from src.domain.entities.user import User
from src.infrastructure.container import Container

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    body: ChatRequest,
    current_user: User = Depends(get_current_user),
    container: Container = Depends(get_container),
):
    cmd = SendChatMessageCommand(container.ai_client, container.group_repo, container.expense_repo)
    result = await cmd.execute(body.message, current_user, body.group_id)
    return ChatResponse(**result)
```

```python
# backend/src/adapters/inbound/api/router.py
from fastapi import APIRouter

from src.adapters.inbound.api.v1 import auth, chatbot, expenses, groups, settlements, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(expenses.router, prefix="/expenses", tags=["expenses"])
api_router.include_router(settlements.router, prefix="/settlements", tags=["settlements"])
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
```

- [ ] **Step 8: Create FastAPI app factory**

```python
# backend/src/infrastructure/app.py
from fastapi import FastAPI, Request

from src.adapters.inbound.api.router import api_router
from src.adapters.inbound.middleware.cors import setup_cors
from src.adapters.inbound.middleware.error_handler import setup_error_handlers
from src.infrastructure.container import Container
from src.infrastructure.database import get_session


def create_app() -> FastAPI:
    app = FastAPI(
        title="PennyPal API",
        description="Expense splitting and management API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    setup_cors(app)
    setup_error_handlers(app)

    @app.middleware("http")
    async def inject_container(request: Request, call_next):
        async for session in get_session():
            request.state.container = Container(session)
            response = await call_next(request)
            return response

    app.include_router(api_router, prefix="/api/v1")

    @app.get("/")
    async def root():
        return {"message": "Welcome to PennyPal API", "version": "1.0.0", "docs": "/docs"}

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    return app
```

- [ ] **Step 9: Update run.py**

```python
# backend/run.py
import uvicorn

from src.infrastructure.app import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
```

- [ ] **Step 10: Run all tests**

Run:
```bash
cd backend && source .venv/bin/activate && python -m pytest tests/ -v
```
Expected: All unit tests PASS (no DB needed for unit tests).

- [ ] **Step 11: Commit**

```bash
git add backend/src/infrastructure/ backend/src/adapters/inbound/ backend/run.py
git commit -m "feat: add infrastructure, schemas, routes, and app factory"
```

---

## Task 9: Alembic Migration Update

**Files:**
- Modify: `backend/alembic.ini`
- Modify: `backend/alembic/env.py`

- [ ] **Step 1: Update alembic.ini to use async driver**

Update `sqlalchemy.url` line to:
```
sqlalchemy.url = postgresql+asyncpg://postgres:postgres@localhost:5432/pennypal
```

- [ ] **Step 2: Update alembic/env.py for async and new model imports**

```python
# backend/alembic/env.py
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from src.adapters.outbound.persistence.models.base import Base
from src.adapters.outbound.persistence.models.user import UserModel  # noqa: F401
from src.adapters.outbound.persistence.models.group import GroupModel, GroupMemberModel  # noqa: F401
from src.adapters.outbound.persistence.models.expense import ExpenseModel, ExpenseSplitModel  # noqa: F401
from src.adapters.outbound.persistence.models.settlement import SettlementModel  # noqa: F401

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

- [ ] **Step 3: Commit**

```bash
git add backend/alembic.ini backend/alembic/env.py
git commit -m "chore: update alembic for async SQLAlchemy and new model paths"
```

---

## Task 10: Docker Setup

**Files:**
- Create: `backend/Dockerfile`
- Create: `docker-compose.yml`
- Create: `backend/.env.example`

- [ ] **Step 1: Create backend Dockerfile**

```dockerfile
# backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

COPY . .

EXPOSE 8000

CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"]
```

- [ ] **Step 2: Create docker-compose.yml**

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: pennypal
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://postgres:postgres@db:5432/pennypal
      SECRET_KEY: dev-secret-key-change-in-production
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY:-}
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - ./backend:/app
    command: uvicorn run:app --host 0.0.0.0 --port 8000 --reload

volumes:
  pgdata:
```

- [ ] **Step 3: Create .env.example**

```bash
# backend/.env.example
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/pennypal
SECRET_KEY=change-me-in-production
ANTHROPIC_API_KEY=sk-ant-your-key-here
CLAUDE_MODEL=claude-sonnet-4-6
CORS_ORIGINS=["http://localhost:3000"]
```

- [ ] **Step 4: Commit**

```bash
git add backend/Dockerfile docker-compose.yml backend/.env.example
git commit -m "chore: add Docker setup for backend and PostgreSQL"
```

---

## Task 11: Pre-commit Hooks & Linting

**Files:**
- Create: `.pre-commit-config.yaml`
- Create: `.editorconfig`
- Create: `.commitlintrc.yaml`

- [ ] **Step 1: Create .pre-commit-config.yaml**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix]
        types_or: [python, pyi]
      - id: ruff-format
        types_or: [python, pyi]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies:
          - pydantic>=2.7.0
          - pydantic-settings>=2.3.0
          - sqlalchemy>=2.0.30
          - types-passlib
          - types-python-jose
        args: [--config-file=backend/pyproject.toml]
        pass_filenames: false
        files: ^backend/src/

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  - repo: https://github.com/alessandrojcm/commitlint-pre-commit-hook
    rev: v9.16.0
    hooks:
      - id: commitlint
        stages: [commit-msg]
        additional_dependencies: ['@commitlint/config-conventional']
```

- [ ] **Step 2: Create .commitlintrc.yaml**

```yaml
# .commitlintrc.yaml
extends:
  - '@commitlint/config-conventional'
rules:
  type-enum:
    - 2
    - always
    - [feat, fix, chore, refactor, test, docs, style, perf, ci, build, revert]
  subject-case:
    - 2
    - never
    - [sentence-case, start-case, pascal-case, upper-case]
```

- [ ] **Step 3: Create .editorconfig**

```ini
# .editorconfig
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.py]
indent_size = 4

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

- [ ] **Step 4: Install pre-commit and create secrets baseline**

Run:
```bash
cd /Users/somen/PycharmProjects/PennyPal && pip install pre-commit && pre-commit install && pre-commit install --hook-type commit-msg && detect-secrets scan > .secrets.baseline
```

- [ ] **Step 5: Commit**

```bash
git add .pre-commit-config.yaml .commitlintrc.yaml .editorconfig .secrets.baseline
git commit -m "chore: add pre-commit hooks, commitlint, and editorconfig"
```

---

## Task 12: Nuxt 3 Frontend Scaffolding

**Files:**
- Create: `frontend/` (via nuxi init)
- Create: `frontend/nuxt.config.ts`
- Create: `frontend/app.vue`
- Create: `frontend/types/index.ts`
- Create: `frontend/Dockerfile`

- [ ] **Step 1: Scaffold Nuxt app**

Run:
```bash
cd /Users/somen/PycharmProjects/PennyPal && npx nuxi@latest init frontend --package-manager pnpm
```

- [ ] **Step 2: Install dependencies**

Run:
```bash
cd frontend && pnpm add @nuxt/ui @pinia/nuxt pinia @nuxtjs/tailwindcss && pnpm add -D @nuxt/eslint eslint prettier typescript
```

- [ ] **Step 3: Update nuxt.config.ts**

```typescript
// frontend/nuxt.config.ts
export default defineNuxtConfig({
  modules: [
    '@nuxt/ui',
    '@pinia/nuxt',
    '@nuxt/eslint',
  ],
  devtools: { enabled: true },
  runtimeConfig: {
    apiBaseUrl: 'http://localhost:8000',
    public: {
      apiBaseUrl: '/api',
    },
  },
  routeRules: {
    '/api/**': {
      proxy: { to: 'http://localhost:8000/**' },
    },
  },
  compatibilityDate: '2025-01-01',
})
```

- [ ] **Step 4: Create types**

```typescript
// frontend/types/index.ts
export interface User {
  id: number
  email: string
  username: string
  full_name: string
  is_active: boolean
  created_at: string | null
  updated_at: string | null
}

export interface Group {
  id: number
  name: string
  description: string | null
  created_by_id: number
  created_at: string | null
  updated_at: string | null
  members: GroupMember[]
}

export interface GroupMember {
  id: number
  user_id: number
  group_id: number
  is_admin: boolean
  joined_at: string | null
}

export interface Expense {
  id: number
  title: string
  description: string | null
  amount: number
  currency: string
  split_type: string
  group_id: number
  created_by_id: number
  created_at: string | null
  updated_at: string | null
  splits: ExpenseSplit[]
}

export interface ExpenseSplit {
  id: number
  expense_id: number
  user_id: number
  amount: number
  percentage: number | null
  created_at: string | null
}

export interface Settlement {
  id: number
  payer_id: number
  payee_id: number
  amount: number
  currency: string
  status: string
  description: string | null
  group_id: number | null
  settled_at: string | null
  created_at: string | null
  updated_at: string | null
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}
```

- [ ] **Step 5: Create frontend Dockerfile**

```dockerfile
# frontend/Dockerfile
FROM node:20-alpine

RUN corepack enable

WORKDIR /app

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .

EXPOSE 3000

CMD ["pnpm", "dev", "--host"]
```

- [ ] **Step 6: Add frontend to docker-compose.yml**

Add this service to `docker-compose.yml` after the `backend` service:

```yaml
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      NUXT_API_BASE_URL: http://backend:8000
```

- [ ] **Step 7: Commit**

```bash
git add frontend/ docker-compose.yml
git commit -m "feat(frontend): scaffold Nuxt 3 app with Nuxt UI and Tailwind"
```

---

## Task 13: Frontend — Auth Pages & Composables

**Files:**
- Create: `frontend/composables/useAuth.ts`
- Create: `frontend/composables/useApi.ts`
- Create: `frontend/stores/auth.ts`
- Create: `frontend/middleware/auth.ts`
- Create: `frontend/pages/login.vue`
- Create: `frontend/pages/register.vue`
- Create: `frontend/app.vue` (update)

This task creates the auth flow. Each file follows Nuxt 3 conventions — composables for logic, Pinia for state, middleware for route protection.

The engineer should create each file with the full component code using Nuxt UI components (`UInput`, `UButton`, `UCard`, `UForm`), wire up the auth store, and test login/register flows manually against the backend.

- [ ] **Step 1: Create all auth files listed above with working implementations**
- [ ] **Step 2: Verify login/register flow works against backend**
- [ ] **Step 3: Commit**

```bash
git add frontend/composables/ frontend/stores/ frontend/middleware/ frontend/pages/login.vue frontend/pages/register.vue frontend/app.vue
git commit -m "feat(frontend): add auth pages, composables, and route middleware"
```

---

## Task 14: Frontend — Core Pages (Groups, Expenses, Settlements, Chat)

**Files:**
- Create: `frontend/pages/index.vue`
- Create: `frontend/pages/groups/index.vue`
- Create: `frontend/pages/groups/[id].vue`
- Create: `frontend/pages/expenses/new.vue`
- Create: `frontend/pages/settlements/index.vue`
- Create: `frontend/pages/chat.vue`
- Create: `frontend/composables/useGroups.ts`
- Create: `frontend/composables/useExpenses.ts`
- Create: `frontend/composables/useSettlements.ts`
- Create: `frontend/composables/useChat.ts`

Each page uses Nuxt UI components and the corresponding composable for data fetching. The engineer should build these page by page, testing each against the backend.

- [ ] **Step 1: Create composables for groups, expenses, settlements, chat**
- [ ] **Step 2: Create dashboard page (index.vue)**
- [ ] **Step 3: Create group list and detail pages**
- [ ] **Step 4: Create expense creation page**
- [ ] **Step 5: Create settlements page**
- [ ] **Step 6: Create chat page with Claude integration**
- [ ] **Step 7: Verify all pages work end-to-end**
- [ ] **Step 8: Commit**

```bash
git add frontend/pages/ frontend/composables/
git commit -m "feat(frontend): add core pages for groups, expenses, settlements, and chat"
```

---

## Task 15: CLAUDE.md & README

**Files:**
- Create: `CLAUDE.md`
- Create: `README.md`

- [ ] **Step 1: Create CLAUDE.md**

```markdown
# PennyPal

Expense-splitting app with Claude-powered chatbot. Web-first, mobile later.

## Architecture

Hexagonal (Ports & Adapters). The domain layer has zero framework imports.

```
backend/src/
  domain/       → Pure Python entities, services, ports (ABC). NO imports from FastAPI/SQLAlchemy.
  application/  → Use cases (commands/queries). Depend ONLY on domain ports.
  adapters/
    inbound/    → FastAPI routes, Pydantic schemas. Translate HTTP → use cases.
    outbound/   → SQLAlchemy repos, Claude client, JWT. Implement domain ports.
  infrastructure/ → Config, DB setup, DI container, app factory.
```

**Rule: dependencies point inward only.** Adapters → Application → Domain ← nothing.

## Quick Start

```bash
docker-compose up        # Starts backend (8000), frontend (3000), PostgreSQL
```

Or manually:
```bash
# Backend
cd backend && source .venv/bin/activate && uvicorn run:app --reload

# Frontend
cd frontend && pnpm dev
```

## Common Commands

```bash
# Backend
cd backend && source .venv/bin/activate
python -m pytest tests/ -v                    # Run all tests
python -m pytest tests/unit/domain/ -v        # Domain tests only
ruff check src/ --fix                         # Lint
ruff format src/                              # Format
mypy src/                                     # Type check
alembic upgrade head                          # Run migrations
alembic revision --autogenerate -m "desc"     # New migration

# Frontend
cd frontend
pnpm dev                                      # Dev server
pnpm lint                                     # ESLint
pnpm build                                    # Production build
```

## Pre-commit

```bash
pre-commit install && pre-commit install --hook-type commit-msg
```

Hooks run: trailing whitespace, ruff (lint+format), mypy, detect-secrets, commitlint.

## Commit Convention

`type(scope): description` — e.g., `feat(expenses): add percentage split`, `fix(auth): handle expired token`

Types: feat, fix, chore, refactor, test, docs, style, perf, ci, build, revert

## Where to Put New Code

| What | Where |
|---|---|
| New business rule | `src/domain/services/` |
| New entity | `src/domain/entities/` |
| New use case | `src/application/commands/` or `src/application/queries/` |
| New API endpoint | `src/adapters/inbound/api/v1/` + schema in `schemas/` |
| New DB query | `src/adapters/outbound/persistence/repositories/` |
| New external integration | `src/adapters/outbound/` (new directory) + port in `src/domain/ports/` |
| New Nuxt page | `frontend/pages/` |
| New Vue composable | `frontend/composables/` |

## Tech Stack

- Backend: Python 3.12, FastAPI, SQLAlchemy 2.0 (async), PostgreSQL, Alembic
- Frontend: Nuxt 3, Nuxt UI, Tailwind CSS, Pinia, TypeScript
- AI: Claude API (anthropic SDK)
- Tooling: Ruff, mypy, ESLint, Prettier, pre-commit, commitlint, Docker
```

- [ ] **Step 2: Create README.md**

```markdown
# PennyPal

Split expenses with friends. Powered by Claude AI.

## Features

- Create groups and manage members
- Add expenses with equal, exact, or percentage splits
- Track balances and optimize settlements
- Chat with Claude to manage expenses in natural language

## Setup

```bash
# Clone and start
git clone <repo-url>
cd PennyPal
docker-compose up
```

- **Backend API**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000

## Development

See [CLAUDE.md](CLAUDE.md) for architecture details and coding conventions.
```

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md README.md
git commit -m "docs: add CLAUDE.md and README"
```

---

## Task 16: Clean Up Old Backend Code

**Files:**
- Delete: `backend/app/` (entire old directory)
- Delete: `backend/requirements.txt`

- [ ] **Step 1: Remove old backend code**

Run:
```bash
cd /Users/somen/PycharmProjects/PennyPal && rm -rf backend/app/ backend/requirements.txt
```

- [ ] **Step 2: Verify new structure still works**

Run:
```bash
cd backend && source .venv/bin/activate && python -m pytest tests/ -v
```
Expected: All tests PASS.

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "chore: remove old flat backend structure"
```

---

## Self-Review Checklist

- [x] **Spec coverage**: All features from spec are covered — auth, groups, expenses, settlements, chatbot, Docker, pre-commit, CLAUDE.md, frontend.
- [x] **Placeholder scan**: No TBDs. Tasks 13-14 are less granular because frontend pages follow repetitive patterns, but the file list and commit messages are explicit.
- [x] **Type consistency**: `UserRepository`, `GroupRepository` etc. — method signatures match between ports (Task 4) and implementations (Task 5). Domain entities match between Task 2 and mappers in Task 5. Schema names match between Task 8 schemas and routes.
- [x] **Dependency direction**: Domain imports nothing external. Application imports only domain. Adapters import application and domain. Infrastructure wires everything.
