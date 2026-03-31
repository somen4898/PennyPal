import pytest
from httpx import ASGITransport, AsyncClient

from src.domain.entities.user import User

TEST_PASSWORD = "Pass1234"  # pragma: allowlist secret


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


@pytest.mark.asyncio
async def test_register(client, mock_container):
    # No existing user with this email or username
    mock_container.user_repo.get_by_email.return_value = None
    mock_container.user_repo.get_by_username.return_value = None
    mock_container.user_repo.create.side_effect = lambda u: User(
        id=10,
        email=u.email,
        username=u.username,
        full_name=u.full_name,
        hashed_password=u.hashed_password,
        is_active=True,
    )

    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "new@test.com",
            "username": "newuser",
            "full_name": "New User",
            "password": TEST_PASSWORD,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 10
    assert data["email"] == "new@test.com"
    assert data["username"] == "newuser"
    assert data["full_name"] == "New User"
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_register_duplicate_email(client, mock_container, test_user):
    # Email already exists
    mock_container.user_repo.get_by_email.return_value = test_user

    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "alice@example.com",
            "username": "newuser",
            "full_name": "New User",
            "password": TEST_PASSWORD,
        },
    )

    assert response.status_code == 409
    assert "already registered" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login(client, mock_container):
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "alice@example.com", "password": TEST_PASSWORD},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["access_token"] == "test_token_123"
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client, mock_container):
    mock_container.auth_provider.verify_password.return_value = False

    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "alice@example.com", "password": "wrongpass"},
    )

    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()
