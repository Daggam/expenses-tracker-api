from fastapi import APIRouter
from src.api.V1 import auth, expenses
api_router = APIRouter()

api_router.include_router(expenses.router)
api_router.include_router(auth.router)