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


@pytest.mark.asyncio
async def test_get_me(client):
    response = await client.get("/api/v1/users/me", headers=AUTH_HEADERS)

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"
    assert data["full_name"] == "Alice Smith"
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_get_me_unauthenticated(client):
    response = await client.get("/api/v1/users/me")

    assert response.status_code in (401, 403)


@pytest.mark.asyncio
async def test_update_me(client):
    response = await client.put(
        "/api/v1/users/me",
        headers=AUTH_HEADERS,
        json={"full_name": "Alice Updated"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Alice Updated"
    assert data["username"] == "alice"


@pytest.mark.asyncio
async def test_list_users(client):
    response = await client.get("/api/v1/users/", headers=AUTH_HEADERS)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    usernames = [u["username"] for u in data]
    assert "alice" in usernames
    assert "bob" in usernames
