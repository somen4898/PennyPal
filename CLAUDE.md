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
