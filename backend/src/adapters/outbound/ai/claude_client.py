from typing import Any

import anthropic
from anthropic.types import MessageParam, TextBlock

from src.domain.ports.ai_client import AiClient


class ClaudeClient(AiClient):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6") -> None:
        self._client = anthropic.AsyncAnthropic(api_key=api_key)
        self._model = model

    async def send_message(
        self, message: str, system_prompt: str, context: list[dict[str, Any]] | None = None
    ) -> str:
        messages: list[MessageParam] = []
        if context:
            for msg in context:
                messages.append(MessageParam(role=msg["role"], content=msg["content"]))
        messages.append(MessageParam(role="user", content=message))

        response = await self._client.messages.create(
            model=self._model,
            max_tokens=1024,
            system=system_prompt,
            messages=messages,
        )
        block = response.content[0]
        if not isinstance(block, TextBlock):
            raise TypeError(f"Expected TextBlock, got {type(block).__name__}")
        return block.text
