import pytest
from httpx import ASGITransport, AsyncClient

from src.domain.entities.group import GroupMember


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
async def test_create_group(client):
    response = await client.post(
        "/api/v1/groups/",
        headers=AUTH_HEADERS,
        json={"name": "Trip", "description": "Fun"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Trip"
    assert data["description"] == "Road trip"  # from get_by_id after create
    assert data["created_by_id"] == 1


@pytest.mark.asyncio
async def test_list_groups(client):
    response = await client.get("/api/v1/groups/", headers=AUTH_HEADERS)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Trip"


@pytest.mark.asyncio
async def test_get_group(client):
    response = await client.get("/api/v1/groups/1", headers=AUTH_HEADERS)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Trip"
    assert len(data["members"]) == 2


@pytest.mark.asyncio
async def test_invite_member(client, mock_container):
    # get_member is called twice in AddGroupMemberCommand:
    # 1) check current_user is admin -> return admin member
    # 2) check invitee is not already a member -> return None
    call_count = 0

    async def get_member_side_effect(group_id, user_id):
        nonlocal call_count
        call_count += 1
        if user_id == 1:
            # Current user (admin check)
            return GroupMember(id=1, group_id=group_id, user_id=1, is_admin=True)
        # Invitee not yet a member
        return None

    mock_container.group_repo.get_member.side_effect = get_member_side_effect

    response = await client.post(
        "/api/v1/groups/1/invite",
        headers=AUTH_HEADERS,
        json={"user_id": 2},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User invited successfully"
