from abc import ABC, abstractmethod
from typing import Any

from src.domain.entities.expense import Expense, ExpenseSplit


class ExpenseRepository(ABC):
    @abstractmethod
    async def get_by_id(self, expense_id: int) -> Expense | None: ...

    @abstractmethod
    async def create(self, expense: Expense) -> Expense: ...

    @abstractmethod
    async def create_splits(self, splits: list[ExpenseSplit]) -> list[ExpenseSplit]: ...

    @abstractmethod
    async def update(self, expense: Expense) -> Expense: ...

    @abstractmethod
    async def delete(self, expense_id: int) -> None: ...

    @abstractmethod
    async def get_by_group(
        self, group_id: int, skip: int = 0, limit: int = 100
    ) -> list[Expense]: ...

    @abstractmethod
    async def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> list[Expense]: ...

    @abstractmethod
    async def get_group_splits(self, group_id: int) -> list[dict[str, Any]]: ...
