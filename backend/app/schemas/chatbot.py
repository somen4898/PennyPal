from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    message: str
    group_id: Optional[int] = None
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    actions_taken: Optional[List[str]] = None
    suggested_actions: Optional[List[Dict[str, Any]]] = None

class ExpenseIntent(BaseModel):
    title: str
    amount: float
    description: Optional[str] = None
    group_id: Optional[int] = None
    split_users: Optional[List[str]] = None  # usernames
    split_type: Optional[str] = "equal"

class SettlementIntent(BaseModel):
    payee_username: str
    amount: float
    description: Optional[str] = None
    group_id: Optional[int] = None