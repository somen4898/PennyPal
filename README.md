# SETTL

> Smart expense splitting with AI-powered natural language processing. Built with a production-grade hexagonal architecture.

[![CI](https://github.com/somen4898/PennyPal/actions/workflows/ci.yml/badge.svg)](https://github.com/somen4898/PennyPal/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-async-009688?logo=fastapi&logoColor=white)
![Nuxt](https://img.shields.io/badge/Nuxt-4-00DC82?logo=nuxtdotjs&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

---

## What It Does

SETTL lets users create groups, add shared expenses, and automatically calculates who owes whom — with an AI chatbot that handles it all through natural language.

**Core capabilities:**

- **Expense Splitting** — equal, exact-amount, or percentage-based splits across group members
- **Settlement Optimization** — greedy algorithm minimizes the number of transactions needed to settle all debts
- **AI Chatbot** — Claude-powered assistant for managing expenses conversationally (e.g. *"Add a $50 dinner split equally"*)
- **Group Management** — create groups, invite members, assign admin roles
- **JWT Authentication** — secure registration/login with hashed passwords and token-based sessions

---

## Architecture

The backend follows **Hexagonal Architecture (Ports & Adapters)** — the domain layer has zero framework imports, making business logic fully testable and framework-independent.

```
backend/src/
├── domain/           # Pure Python: entities, services, ports (ABCs)
│   ├── entities/     # User, Group, Expense, Settlement, ExpenseSplit
│   ├── services/     # Split calculation, balance computation, settlement optimization
│   ├── ports/        # Abstract interfaces (repos, auth, AI client)
│   └── exceptions.py # Domain-specific errors
│
├── application/      # Use cases — depend ONLY on domain ports
│   ├── commands/     # CreateExpense, CreateGroup, RegisterUser, SendChatMessage...
│   └── queries/      # GetBalances, GetSettlementSuggestions, GetGroupExpenses...
│
├── adapters/
│   ├── inbound/      # FastAPI routes, Pydantic schemas, middleware
│   └── outbound/     # SQLAlchemy repos, JWT provider, Claude client
│
└── infrastructure/   # DI container, database config, app factory
```

**Dependency rule:** Adapters → Application → Domain ← nothing.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.12, FastAPI (async), SQLAlchemy 2.0 (async ORM), Pydantic v2 |
| **Frontend** | Nuxt 4, Vue 3, Tailwind CSS v4, Nuxt UI, Pinia, TypeScript |
| **Database** | PostgreSQL 16, Alembic migrations |
| **AI** | Anthropic Claude API (context-aware chatbot) |
| **Auth** | JWT (python-jose) + bcrypt password hashing |
| **DevOps** | Docker Compose, GitHub Actions CI/CD, pre-commit hooks |
| **Quality** | Ruff (lint/format), mypy (strict), ESLint, Prettier, commitlint, pytest |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/auth/register` | Register a new user |
| `POST` | `/v1/auth/login` | Login and receive JWT |
| `GET` | `/v1/users/me` | Get current user |
| `POST` | `/v1/groups/` | Create a group |
| `GET` | `/v1/groups/` | List user's groups |
| `POST` | `/v1/groups/{id}/invite` | Invite a member |
| `POST` | `/v1/expenses/` | Create an expense with splits |
| `GET` | `/v1/expenses/group/{id}` | List group expenses |
| `GET` | `/v1/settlements/group/{id}/balances` | Get computed balances |
| `GET` | `/v1/settlements/group/{id}/suggestions` | Get optimized settlement plan |
| `POST` | `/v1/chatbot/chat` | Send message to AI assistant |

Full interactive docs available at `/docs` (Swagger UI) when running locally.

---

## Getting Started

### With Docker (recommended)

```bash
git clone https://github.com/somen4898/PennyPal.git
cd PennyPal
docker-compose up
```

- **Backend API:** http://localhost:8000/docs
- **Frontend:** http://localhost:3000

### Manual Setup

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn run:app --reload

# Frontend
cd frontend
pnpm install
pnpm dev
```

### Environment Variables

Create a `.env` file in `backend/`:

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/settl  # pragma: allowlist secret
SECRET_KEY=your-secret-key
ANTHROPIC_API_KEY=your-claude-api-key
```

---

## Testing

```bash
# Backend — unit + integration tests with async PostgreSQL
cd backend && source .venv/bin/activate
python -m pytest tests/ -v

# Domain-only (pure logic, no DB)
python -m pytest tests/unit/domain/ -v

# Frontend
cd frontend && pnpm test
```

The CI pipeline runs on every push and PR — backend tests against a live PostgreSQL instance, frontend builds are verified, and linting/formatting is enforced.

---

## Project Structure

```
PennyPal/
├── backend/
│   ├── src/                # Application source (hexagonal layout)
│   ├── tests/              # 26 test files (unit + integration)
│   ├── alembic/            # Database migrations
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── pages/              # 8 routes (dashboard, groups, settlements, chat, auth)
│   ├── stores/             # Pinia state management
│   ├── composables/        # Shared logic (API client, validation)
│   ├── assets/css/         # Custom theming & animations
│   ├── Dockerfile
│   └── nuxt.config.ts
├── .github/workflows/      # CI/CD + auto-labeling
├── docker-compose.yml
└── CLAUDE.md               # Architecture conventions
```

---

## Engineering Highlights

- **Fully async** — FastAPI + SQLAlchemy async sessions end-to-end, no blocking I/O
- **Strict typing** — mypy strict mode on backend, TypeScript on frontend
- **Domain isolation** — business logic has zero coupling to frameworks or databases
- **Transaction safety** — explicit `session.begin()` with rollback on errors
- **Settlement optimization** — greedy algorithm reduces N debts to minimal transactions
- **CI enforcement** — ruff, mypy, pytest, ESLint, commitlint all run in GitHub Actions
- **Conventional commits** — enforced via commitlint pre-commit hook
- **Dark luxury UI** — CRED-inspired design with custom typography (DM Sans, DM Serif Display) and accent palette
