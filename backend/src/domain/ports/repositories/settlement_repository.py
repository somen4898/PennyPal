from abc import ABC, abstractmethod

from src.domain.entities.settlement import Settlement


class SettlementRepository(ABC):
    @abstractmethod
    async def get_by_id(self, settlement_id: int) -> Settlement | None: ...

    @abstractmethod
    async def create(self, settlement: Settlement) -> Settlement: ...

    @abstractmethod
    async def update(self, settlement: Settlement) -> Settlement: ...

    @abstractmethod
    async def delete(self, settlement_id: int) -> None: ...

    @abstractmethod
    async def get_by_user(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Settlement]: ...

    @abstractmethod
    async def get_by_group(
        self, group_id: int, skip: int = 0, limit: int = 100
    ) -> list[Settlement]: ...
