from abc import ABC, abstractmethod

from src.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None: ...

    @abstractmethod
    async def create(self, user: User) -> User: ...

    @abstractmethod
    async def update(self, user: User) -> User: ...

    @abstractmethod
    async def get_by_ids(self, user_ids: list[int]) -> list[User]: ...

    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100) -> list[User]: ...
