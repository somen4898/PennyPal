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


async def test_chat(client: AsyncClient):
    payload = {"message": "What do I owe?"}
    response = await client.post("/api/v1/chatbot/chat", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["response"] == "Hello! How can I help?"


async def test_chat_with_group(client: AsyncClient):
    payload = {"message": "Show balances", "group_id": 1}
    response = await client.post("/api/v1/chatbot/chat", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
