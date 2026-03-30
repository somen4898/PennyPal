from fastapi import APIRouter

from src.adapters.inbound.api.deps import get_container, get_current_user
from src.adapters.inbound.schemas.chatbot import ChatRequest, ChatResponse
from src.application.commands.send_chat_message import SendChatMessageCommand
from src.domain.entities.user import User
from src.infrastructure.container import Container

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    body: ChatRequest,
    current_user: User = get_current_user,
    container: Container = get_container,
):
    cmd = SendChatMessageCommand(container.ai_client, container.group_repo, container.expense_repo)
    result = await cmd.execute(body.message, current_user, body.group_id)
    return ChatResponse(**result)
