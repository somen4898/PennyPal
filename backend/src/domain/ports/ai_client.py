from abc import ABC, abstractmethod
from typing import Any


class AiClient(ABC):
    @abstractmethod
    async def send_message(
        self, message: str, system_prompt: str, context: list[dict[str, Any]] | None = None
    ) -> str: ...
