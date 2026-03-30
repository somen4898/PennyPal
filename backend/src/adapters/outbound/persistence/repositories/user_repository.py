from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.outbound.persistence.mappers.user_mapper import UserMapper
from src.adapters.outbound.persistence.models.user import UserModel
from src.domain.entities.user import User
from src.domain.ports.repositories.user_repository import UserRepository


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self._session.execute(select(UserModel).where(UserModel.id == user_id))
        model = result.scalar_one_or_none()
        return UserMapper.to_domain(model) if model else None

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(select(UserModel).where(UserModel.email == email))
        model = result.scalar_one_or_none()
        return UserMapper.to_domain(model) if model else None

    async def get_by_username(self, username: str) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        model = result.scalar_one_or_none()
        return UserMapper.to_domain(model) if model else None

    async def create(self, user: User) -> User:
        model = UserMapper.to_model(user)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return UserMapper.to_domain(model)

    async def update(self, user: User) -> User:
        result = await self._session.execute(select(UserModel).where(UserModel.id == user.id))
        model = result.scalar_one()
        model.email = user.email
        model.username = user.username
        model.full_name = user.full_name
        model.hashed_password = user.hashed_password
        model.is_active = user.is_active
        await self._session.flush()
        await self._session.refresh(model)
        return UserMapper.to_domain(model)

    async def list_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        result = await self._session.execute(select(UserModel).offset(skip).limit(limit))
        return [UserMapper.to_domain(m) for m in result.scalars().all()]
