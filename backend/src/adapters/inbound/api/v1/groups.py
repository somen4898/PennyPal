from fastapi import APIRouter

from src.adapters.inbound.api.deps import get_container, get_current_user
from src.adapters.inbound.schemas.group import (
    GroupCreateRequest,
    GroupInviteRequest,
    GroupMemberResponse,
    GroupResponse,
    GroupUpdateRequest,
)
from src.application.commands.add_group_member import AddGroupMemberCommand
from src.application.commands.create_group import CreateGroupCommand
from src.application.queries.get_user_groups import GetUserGroupsQuery
from src.domain.entities.group import Group
from src.domain.entities.user import User
from src.domain.exceptions import ForbiddenError, NotFoundError
from src.infrastructure.container import Container

router = APIRouter()


def _group_response(group: Group) -> GroupResponse:
    members = [
        GroupMemberResponse(
            id=m.id,
            user_id=m.user_id,
            group_id=m.group_id,
            is_admin=m.is_admin,
            joined_at=m.joined_at,
        )
        for m in (group.members or [])
    ]
    return GroupResponse(
        id=group.id,
        name=group.name,
        description=group.description,
        created_by_id=group.created_by_id,
        created_at=group.created_at,
        updated_at=group.updated_at,
        members=members,
    )


@router.post("/", response_model=GroupResponse)
async def create_group(
    body: GroupCreateRequest,
    current_user: User = get_current_user,
    container: Container = get_container,
):
    cmd = CreateGroupCommand(container.group_repo)
    group = await cmd.execute(body.name, body.description, current_user.id)
    return _group_response(group)


@router.get("/", response_model=list[GroupResponse])
async def list_groups(
    current_user: User = get_current_user,
    container: Container = get_container,
):
    query = GetUserGroupsQuery(container.group_repo)
    groups = await query.execute(current_user.id)
    return [_group_response(g) for g in groups]


@router.get("/{group_id}", response_model=GroupResponse)
async def get_group(
    group_id: int,
    current_user: User = get_current_user,
    container: Container = get_container,
):
    group = await container.group_repo.get_by_id(group_id)
    if not group:
        raise NotFoundError("Group not found")
    member = await container.group_repo.get_member(group_id, current_user.id)
    if not member:
        raise ForbiddenError("Not a member of this group")
    return _group_response(group)


@router.put("/{group_id}", response_model=GroupResponse)
async def update_group(
    group_id: int,
    body: GroupUpdateRequest,
    current_user: User = get_current_user,
    container: Container = get_container,
):
    group = await container.group_repo.get_by_id(group_id)
    if not group:
        raise NotFoundError("Group not found")
    member = await container.group_repo.get_member(group_id, current_user.id)
    if not member or not member.is_admin:
        raise ForbiddenError("Only group admins can update group details")

    if body.name is not None:
        group.name = body.name
    if body.description is not None:
        group.description = body.description
    updated = await container.group_repo.update(group)
    return _group_response(updated)


@router.post("/{group_id}/invite")
async def invite_member(
    group_id: int,
    body: GroupInviteRequest,
    current_user: User = get_current_user,
    container: Container = get_container,
):
    cmd = AddGroupMemberCommand(container.group_repo, container.user_repo)
    await cmd.execute(group_id, body.user_id, body.is_admin, current_user.id)
    return {"message": "User invited successfully"}


@router.delete("/{group_id}/members/{user_id}")
async def remove_member(
    group_id: int,
    user_id: int,
    current_user: User = get_current_user,
    container: Container = get_container,
):
    group = await container.group_repo.get_by_id(group_id)
    if not group:
        raise NotFoundError("Group not found")

    if user_id != current_user.id:
        member = await container.group_repo.get_member(group_id, current_user.id)
        if not member or not member.is_admin:
            raise ForbiddenError("Only group admins can remove other users")

    await container.group_repo.remove_member(group_id, user_id)
    return {"message": "User removed from group successfully"}
