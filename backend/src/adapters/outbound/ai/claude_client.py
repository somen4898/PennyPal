import anthropic

from src.domain.ports.ai_client import AiClient


class ClaudeClient(AiClient):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6") -> None:
        self._client = anthropic.AsyncAnthropic(api_key=api_key)
        self._model = model

    async def send_message(
        self, message: str, system_prompt: str, context: list[dict] | None = None
    ) -> str:
        messages: list[dict] = []
        if context:
            messages.extend(context)
        messages.append({"role": "user", "content": message})

        response = await self._client.messages.create(
            model=self._model,
            max_tokens=1024,
            system=system_prompt,
            messages=messages,
        )
        return response.content[0].text