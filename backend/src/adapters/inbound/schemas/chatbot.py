from typing import Any

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    group_id: int | None = None


class ChatResponse(BaseModel):
    response: str
    actions_taken: list[str] = []
    suggested_actions: list[dict[str, Any]] = []
