# PennyPal — Full Restructure Design Spec

**Date:** 2026-03-30
**Status:** Approved
**Scope:** Complete architectural restructure of PennyPal — hexagonal architecture, Nuxt 3 frontend, FastAPI backend, Docker, pre-commit hooks, CLAUDE.md

---

## 1. Overview

PennyPal is an expense-splitting and group settlement app (Splitwise-style) with a Claude-powered conversational interface. The existing backend has working business logic but lacks a frontend, tests, tooling, and proper architectural boundaries. This spec covers a complete restructure into a clean hexagonal architecture.

**Core features (unchanged):**
- User registration and JWT authentication
- Group creation and member management
- Expense creation with equal/exact/percentage splits
- Settlement tracking with balance optimization
- Claude API-powered chatbot for natural language expense management

---

## 2. Tech Stack

| Layer | Technology | Rationale |
|---|---|---|
| Frontend | Nuxt 3 + Nuxt UI + Tailwind CSS | Official Nuxt team stack, cohesive, Tailwind-based, great DX |
| Backend | Python 3.12 + FastAPI | Async, strong typing with Pydantic, existing logic preserved |
| ORM | SQLAlchemy 2.0 (async) | ACID transactions critical for financial data |
| Database | PostgreSQL | Relational integrity for expense splits and settlements |
| AI/Chatbot | Claude API (anthropic SDK) | Replaces regex-based chatbot |
| Auth | JWT (python-jose + bcrypt) | Existing, works well |
| Migrations | Alembic | Existing, carry forward |
| Containerization | Docker + Docker Compose | Portable, deployment-agnostic |

---

## 3. Architecture: Full Hexagonal (Ports & Adapters)

**Core principle:** The domain layer has zero imports from any framework. Dependencies always point inward — adapters depend on application, application depends on domain, domain depends on nothing.

### 3.1 Backend Directory Structure

```
backend/
├── src/
│   ├── domain/                        # PURE — no framework imports
│   │   ├── entities/
│   │   │   ├── user.py                # User dataclass
│   │   │   ├── group.py               # Group, GroupMember dataclasses
│   │   │   ├── expense.py             # Expense, ExpenseSplit, SplitType enum
│   │   │   └── settlement.py          # Settlement, SettlementStatus enum
│   │   ├── services/
│   │   │   ├── expense_service.py     # Split calculation logic (pure functions)
│   │   │   ├── settlement_service.py  # Balance optimization (greedy algorithm)
│   │   │   └── chatbot_service.py     # Intent parsing, conversation logic
│   │   ├── ports/
│   │   │   ├── repositories/
│   │   │   │   ├── user_repository.py
│   │   │   │   ├── group_repository.py
│   │   │   │   ├── expense_repository.py
│   │   │   │   └── settlement_repository.py
│   │   │   ├── ai_client.py           # Abstract AI interface
│   │   │   └── auth_provider.py       # Abstract auth interface
│   │   └── exceptions.py              # DomainError, NotFoundError, UnauthorizedError, ValidationError
│   │
│   ├── application/                   # USE CASES — orchestrates domain, no framework deps
│   │   ├── commands/
│   │   │   ├── register_user.py
│   │   │   ├── login_user.py
│   │   │   ├── create_group.py
│   │   │   ├── add_group_member.py
│   │   │   ├── create_expense.py
│   │   │   ├── create_settlement.py
│   │   │   └── send_chat_message.py
│   │   └── queries/
│   │       ├── get_user_groups.py
│   │       ├── get_group_expenses.py
│   │       ├── get_balances.py
│   │       └── get_settlement_suggestions.py
│   │
│   ├── adapters/
│   │   ├── inbound/                   # DRIVING adapters — translate external requests to use cases
│   │   │   ├── api/
│   │   │   │   ├── v1/
│   │   │   │   │   ├── auth.py
│   │   │   │   │   ├── users.py
│   │   │   │   │   ├── groups.py
│   │   │   │   │   ├── expenses.py
│   │   │   │   │   ├── settlements.py
│   │   │   │   │   └── chatbot.py
│   │   │   │   └── router.py          # Aggregates all v1 routes
│   │   │   ├── schemas/               # Pydantic request/response models (NOT domain entities)
│   │   │   │   ├── user.py
│   │   │   │   ├── group.py
│   │   │   │   ├── expense.py
│   │   │   │   ├── settlement.py
│   │   │   │   └── chatbot.py
│   │   │   └── middleware/
│   │   │       ├── cors.py
│   │   │       └── error_handler.py   # Maps DomainError → HTTP status codes
│   │   │
│   │   └── outbound/                  # DRIVEN adapters — implement ports
│   │       ├── persistence/
│   │       │   ├── models/            # SQLAlchemy ORM models (separate from domain entities)
│   │       │   │   ├── user.py
│   │       │   │   ├── group.py
│   │       │   │   ├── expense.py
│   │       │   │   └── settlement.py
│   │       │   ├── repositories/      # Concrete implementations of domain ports
│   │       │   │   ├── user_repository.py
│   │       │   │   ├── group_repository.py
│   │       │   │   ├── expense_repository.py
│   │       │   │   └── settlement_repository.py
│   │       │   └── mappers/           # Convert ORM model ↔ domain entity
│   │       │       ├── user_mapper.py
│   │       │       ├── group_mapper.py
│   │       │       ├── expense_mapper.py
│   │       │       └── settlement_mapper.py
│   │       ├── ai/
│   │       │   └── claude_client.py   # Implements ai_client.py port using anthropic SDK
│   │       └── auth/
│   │           └── jwt_provider.py    # Implements auth_provider.py port using python-jose
│   │
│   └── infrastructure/
│       ├── config.py                  # Pydantic settings (from env vars)
│       ├── database.py                # Async engine, session factory, connection pooling
│       ├── container.py               # Dependency injection — wires ports to implementations
│       └── app.py                     # FastAPI app factory (registers routers, middleware)
│
├── alembic/
│   ├── env.py
│   └── versions/
├── tests/
│   ├── unit/
│   │   ├── domain/                    # Pure logic, no DB, no framework
│   │   └── application/               # Use cases with mocked ports
│   ├── integration/
│   │   └── adapters/                  # Repos + API against real PostgreSQL
│   └── conftest.py
├── alembic.ini
├── pyproject.toml                     # All Python config: deps, ruff, mypy, pytest
├── Dockerfile
└── run.py
```

### 3.2 Frontend Directory Structure

```
frontend/
├── nuxt.config.ts
├── app.vue
├── pages/
│   ├── index.vue                      # Dashboard: balances, recent activity, quick actions
│   ├── login.vue
│   ├── register.vue
│   ├── groups/
│   │   ├── index.vue                  # Group list
│   │   └── [id].vue                  # Group detail: members, expenses, balances
│   ├── expenses/
│   │   └── new.vue                   # Create expense: split type selector
│   ├── settlements/
│   │   └── index.vue                 # Who owes whom + settle up actions
│   └── chat.vue                       # Claude chatbot interface
├── components/
│   ├── expense/
│   ├── group/
│   ├── settlement/
│   ├── chat/
│   └── ui/                            # Shared UI primitives
├── composables/
│   ├── useAuth.ts                     # JWT management, login/logout
│   ├── useGroups.ts
│   ├── useExpenses.ts
│   ├── useSettlements.ts
│   └── useChat.ts
├── stores/
│   ├── auth.ts                        # Pinia: persisted auth state
│   └── notifications.ts               # Pinia: toast/alert state
├── server/
│   └── api/                           # Nuxt server routes proxy to backend (avoids CORS)
├── middleware/
│   └── auth.ts                        # Protects authenticated routes
├── types/
│   └── index.ts                       # Shared TypeScript interfaces
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── Dockerfile
```

---

## 4. Request Lifecycle (Data Flow)

```
HTTP Request
  → FastAPI Route (inbound adapter)
    → Pydantic Schema (input validation)
      → Use Case Command/Query (application layer)
        → Domain Service (pure business logic)
          → Port interface (abstract)
            → Repository / Claude Client (outbound adapter)
              → PostgreSQL / Claude API
                → ORM Model → Mapper → Domain Entity → Response Schema → JSON
```

**Dependency direction — always inward:**
- Adapters → Application → Domain ← nothing

**DI wiring in `container.py`:**
```python
expense_repo = SqlAlchemyExpenseRepository(session)
expense_service = ExpenseService()
create_expense_cmd = CreateExpenseCommand(expense_repo, expense_service)
```
Constructor injection only — no framework magic, fully testable.

---

## 5. Authentication

- JWT tokens (HS256) issued on login
- Stored in httpOnly cookie (set via Nuxt server route) — not localStorage
- FastAPI verifies token via `JwtProvider` (outbound adapter implementing `AuthProvider` port)
- Route middleware in Nuxt protects authenticated pages
- Token refresh handled by `useAuth` composable

---

## 6. Claude API Chatbot

- `ClaudeClient` (outbound adapter) implements `AiClient` port
- Uses `anthropic` Python SDK with `claude-opus-4-6` or `claude-sonnet-4-6`
- `ChatbotService` (domain) handles conversation context and intent
- `SendChatMessageCommand` (application) orchestrates: parse intent → look up data → call Claude → return response
- System prompt gives Claude context about the user's groups, balances, and recent expenses
- Streamed responses for better UX

---

## 7. Tooling & Code Quality

### Backend (pyproject.toml)
- **Ruff** — linter + formatter (replaces flake8, isort, black)
- **mypy** — strict type checking (`strict = true`)
- **pytest + pytest-asyncio + pytest-cov** — test runner with async support and coverage

### Frontend
- **ESLint** with `@nuxt/eslint-config`
- **Prettier** — formatting for TS/Vue/CSS
- **TypeScript strict mode** — `"strict": true` in tsconfig

### Pre-commit Hooks (`.pre-commit-config.yaml`)
1. `trailing-whitespace`, `end-of-file-fixer`, `check-yaml`, `check-json` — hygiene
2. `ruff` — Python lint + format
3. `mypy` — Python type check
4. `eslint` — TypeScript/Vue lint
5. `prettier` — TypeScript/Vue/CSS format
6. `commitlint` — enforce conventional commits (`feat:`, `fix:`, `chore:`, `refactor:`, `test:`, `docs:`)
7. `detect-secrets` — block accidental credential commits

### Commit Convention
`type(scope): description`
e.g., `feat(expenses): add percentage split calculation`
e.g., `fix(auth): handle expired token refresh`

---

## 8. Testing Strategy

### Backend
| Layer | Type | Tooling | What's tested |
|---|---|---|---|
| `domain/` | Unit | pytest | Split calculations, balance optimization, pure logic |
| `application/` | Unit | pytest + mocks | Use case orchestration with fake repos |
| `adapters/` | Integration | pytest + real DB | Repository CRUD, full API request/response |

**Coverage target:** 80%+ on domain and application layers.

### Frontend
- **Vitest** — unit tests for composables and Pinia stores
- **Playwright** — E2E tests for critical flows: login → group → expense → settle

---

## 9. Docker Compose

```yaml
services:
  backend:   # FastAPI, port 8000, hot reload in dev
  frontend:  # Nuxt, port 3000, hot reload in dev
  db:        # PostgreSQL 16
```

Single `docker-compose up` to run the full stack locally.

---

## 10. CLAUDE.md Contents

The CLAUDE.md at project root will cover:
- Project overview and what PennyPal does
- Architecture explanation: hexagonal, ports/adapters, which layer does what
- Directory guide: where to put new code
- Hexagonal rules: what imports are forbidden in each layer
- Running the project: `docker-compose up`
- Pre-commit setup: `pre-commit install`
- Common commands: run tests, lint, migrate DB
- Coding conventions: naming, type hints required, no `any` in TS
- Claude API usage: model choice, streaming pattern

---

## 11. What's Being Replaced / Removed

| Current | Replaced by |
|---|---|
| `backend/app/` flat structure | Hexagonal `backend/src/` structure |
| `requirements.txt` | `pyproject.toml` |
| No linting | Ruff + mypy + ESLint + Prettier |
| No pre-commit hooks | `.pre-commit-config.yaml` with 7 hooks |
| No frontend | Nuxt 3 + Nuxt UI + Tailwind |
| No tests | pytest (unit + integration) + Vitest + Playwright |
| No Docker | `Dockerfile` × 2 + `docker-compose.yml` |
| No CLAUDE.md | Comprehensive `CLAUDE.md` at root |
| Regex chatbot | Claude API (`claude-sonnet-4-6`) |
| No README | `README.md` with setup instructions |
