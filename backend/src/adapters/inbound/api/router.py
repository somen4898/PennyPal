from fastapi import APIRouter

from src.adapters.inbound.api.v1 import auth, chatbot, expenses, groups, settlements, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(expenses.router, prefix="/expenses", tags=["expenses"])
api_router.include_router(settlements.router, prefix="/settlements", tags=["settlements"])
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
