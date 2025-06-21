from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .groups import router as groups_router
from .expenses import router as expenses_router
from .settlements import router as settlements_router
from .chatbot import router as chatbot_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(groups_router, prefix="/groups", tags=["groups"])
api_router.include_router(expenses_router, prefix="/expenses", tags=["expenses"])
api_router.include_router(settlements_router, prefix="/settlements", tags=["settlements"])
api_router.include_router(chatbot_router, prefix="/chatbot", tags=["chatbot"])