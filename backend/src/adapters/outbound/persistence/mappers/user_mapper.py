from src.adapters.outbound.persistence.models.user import UserModel
from src.domain.entities.user import User


class UserMapper:
    @staticmethod
    def to_domain(model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            username=model.username,
            full_name=model.full_name,
            hashed_password=model.hashed_password,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: User) -> UserModel:
        return UserModel(
            id=entity.id if entity.id else None,
            email=entity.email,
            username=entity.username,
            full_name=entity.full_name,
            hashed_password=entity.hashed_password,
            is_active=entity.is_active,
        )
