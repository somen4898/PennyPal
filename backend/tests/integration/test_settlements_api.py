import pytest
from httpx import ASGITransport, AsyncClient


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


async def test_create_settlement(client: AsyncClient):
    payload = {
        "payee_id": 2,
        "amount": "50.00",
    }
    response = await client.post("/api/v1/settlements/", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["payer_id"] == 1  # current user
    assert data["payee_id"] == 2
    assert data["status"] == "pending"


async def test_list_settlements(client: AsyncClient):
    response = await client.get("/api/v1/settlements/", headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


async def test_get_balances(client: AsyncClient):
    response = await client.get("/api/v1/settlements/group/1/balances", headers=AUTH_HEADERS)
    assert response.status_code == 200


async def test_get_suggestions(client: AsyncClient):
    response = await client.get("/api/v1/settlements/group/1/suggestions", headers=AUTH_HEADERS)
    assert response.status_code == 200


async def test_update_settlement(client: AsyncClient):
    """settlement.payer_id=2, payee_id=1. Current user is id=1 (payee), so update is allowed."""
    payload = {
        "description": "Paid via UPI",
    }
    response = await client.put("/api/v1/settlements/1", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Paid via UPI"


async def test_delete_settlement_not_payer(client: AsyncClient):
    """settlement.payer_id=2, current_user.id=1 so deletion should be forbidden."""
    response = await client.delete("/api/v1/settlements/1", headers=AUTH_HEADERS)
    assert response.status_code == 403
