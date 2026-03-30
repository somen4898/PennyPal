from decimal import Decimal

import pytest
from httpx import ASGITransport, AsyncClient

from src.domain.entities.expense import Expense, ExpenseSplit, SplitType


@pytest.fixture
def app(mock_container):
    from fastapi import FastAPI, Request

    from src.adapters.inbound.api.router import api_router
    from src.adapters.inbound.middleware.error_handler import setup_error_handlers

    app = FastAPI()
    setup_error_handlers(app)

    @app.middleware("http")
    async def inject_mock_container(request: Request, call_next):
        request.state.container = mock_container
        response = await call_next(request)
        return response

    app.include_router(api_router, prefix="/api/v1")
    return app


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


AUTH_HEADERS = {"Authorization": "Bearer test_token_123"}


async def test_create_expense(client: AsyncClient):
    payload = {
        "title": "Dinner",
        "amount": "200.00",
        "group_id": 1,
        "split_type": "equal",
        "splits": [
            {"user_id": 1},
            {"user_id": 2},
        ],
    }
    response = await client.post("/api/v1/expenses/", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Lunch"  # returned from mock get_by_id
    assert data["group_id"] == 1


async def test_get_group_expenses(client: AsyncClient):
    response = await client.get("/api/v1/expenses/group/1", headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


async def test_get_expense(client: AsyncClient):
    response = await client.get("/api/v1/expenses/1", headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Lunch"


async def test_delete_expense(client: AsyncClient):
    response = await client.delete("/api/v1/expenses/1", headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Expense deleted successfully"


async def test_delete_expense_not_creator(client: AsyncClient, mock_container):
    """Current user has id=1 but expense.created_by_id=999, so deletion should be forbidden."""
    mock_container.expense_repo.get_by_id.return_value = Expense(
        id=1,
        title="Lunch",
        amount=Decimal("100.00"),
        group_id=1,
        created_by_id=999,
        split_type=SplitType.EQUAL,
        splits=[
            ExpenseSplit(id=1, expense_id=1, user_id=1, amount=Decimal("50.00")),
            ExpenseSplit(id=2, expense_id=1, user_id=2, amount=Decimal("50.00")),
        ],
    )
    response = await client.delete("/api/v1/expenses/1", headers=AUTH_HEADERS)
    assert response.status_code == 403
