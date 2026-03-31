# SETTL — Development Commands

# Start everything (backend + frontend)
dev:
    #!/usr/bin/env bash
    # Kill any existing processes on our ports
    lsof -t -i:8000 -i:3000 2>/dev/null | xargs kill 2>/dev/null
    sleep 1

    echo "Starting SETTL..."
    echo ""
    echo "  Backend  → http://localhost:8000"
    echo "  Frontend → http://localhost:3000"
    echo "  API Docs → http://localhost:8000/docs"
    echo ""

    # Start backend in background
    cd backend && source .venv/bin/activate && uvicorn run:app --reload --port 8000 --loop asyncio &
    BACKEND_PID=$!

    # Start frontend in foreground (so Ctrl+C works)
    cd frontend && NUXT_TELEMETRY_DISABLED=1 pnpm dev &
    FRONTEND_PID=$!

    # Wait for either to exit, kill both on Ctrl+C
    trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
    wait

# Backend only
backend:
    cd backend && source .venv/bin/activate && uvicorn run:app --reload --port 8000 --loop asyncio

# Frontend only
frontend:
    cd frontend && NUXT_TELEMETRY_DISABLED=1 pnpm dev

# Run all backend tests
test:
    cd backend && source .venv/bin/activate && python -m pytest tests/ -v

# Run unit tests only
test-unit:
    cd backend && source .venv/bin/activate && python -m pytest tests/unit/ -v

# Run integration tests only
test-integration:
    cd backend && source .venv/bin/activate && python -m pytest tests/integration/ -v

# Run frontend tests
test-frontend:
    cd frontend && pnpm test

# Lint backend
lint:
    cd backend && source .venv/bin/activate && ruff check src/ tests/

# Format backend
format:
    cd backend && source .venv/bin/activate && ruff format src/ tests/

# Run database migrations
migrate:
    cd backend && source .venv/bin/activate && alembic upgrade head

# Create a new migration
migrate-new message:
    cd backend && source .venv/bin/activate && alembic revision --autogenerate -m "{{message}}"

# Install all dependencies
install:
    cd backend && source .venv/bin/activate && pip install -e ".[dev]"
    cd frontend && pnpm install

# Build frontend for production
build:
    cd frontend && pnpm build

# Stop all dev processes
stop:
    lsof -t -i:8000 -i:3000 2>/dev/null | xargs kill 2>/dev/null && echo "Stopped" || echo "Nothing running"
