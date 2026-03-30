from src.adapters.outbound.persistence.models.group import GroupMemberModel, GroupModel
from src.domain.entities.group import Group, GroupMember


class GroupMapper:
    @staticmethod
    def to_domain(model: GroupModel) -> Group:
        members = [GroupMemberMapper.to_domain(m) for m in model.members] if model.members else None
        return Group(
            id=model.id,
            name=model.name,
            description=model.description,
            created_by_id=model.created_by_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            members=members,
        )

    @staticmethod
    def to_model(entity: Group) -> GroupModel:
        return GroupModel(
            id=entity.id if entity.id else None,
            name=entity.name,
            description=entity.description,
            created_by_id=entity.created_by_id,
        )


class GroupMemberMapper:
    @staticmethod
    def to_domain(model: GroupMemberModel) -> GroupMember:
        return GroupMember(
            id=model.id,
            group_id=model.group_id,
            user_id=model.user_id,
            is_admin=model.is_admin,
            joined_at=model.joined_at,
        )

    @staticmethod
    def to_model(entity: GroupMember) -> GroupMemberModel:
        return GroupMemberModel(
            id=entity.id if entity.id else None,
            group_id=entity.group_id,
            user_id=entity.user_id,
            is_admin=entity.is_admin,
        )
