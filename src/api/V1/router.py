from fastapi import APIRouter
from src.api.V1 import expenses
api_router = APIRouter()

api_router.include_router(expenses.router)