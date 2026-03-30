# SETTL — Development Commands

# Start everything (backend + frontend)
dev:
    #!/usr/bin/env bash
    echo "Starting SETTL..."
    echo ""
    echo "  Backend  → http://localhost:8000"
    echo "  Frontend → http://localhost:3000"
    echo "  API Docs → http://localhost:8000/docs"
    echo ""

    # Start backend in background
    cd backend && source .venv/bin/activate && uvicorn run:app --reload --port 8000 &
    BACKEND_PID=$!

    # Start frontend in background
    cd frontend && pnpm dev &
    FRONTEND_PID=$!

    # Wait for either to exit
    trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
    wait

# Backend only
backend:
    cd backend && source .venv/bin/activate && uvicorn run:app --reload --port 8000

# Frontend only
frontend:
    cd frontend && pnpm dev

# Run all backend tests
test:
    cd backend && source .venv/bin/activate && python -m pytest tests/ -v

# Run unit tests only
test-unit:
    cd backend && source .venv/bin/activate && python -m pytest tests/unit/ -v

# Run integration tests only
test-integration:
    cd backend && source .venv/bin/activate && python -m pytest tests/integration/ -v

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
