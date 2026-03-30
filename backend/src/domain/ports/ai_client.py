from abc import ABC, abstractmethod


class AiClient(ABC):
    @abstractmethod
    async def send_message(
        self, message: str, system_prompt: str, context: list[dict] | None = None
    ) -> str: ...
