from fastapi import APIRouter, Depends, Query,HTTPException
from typing import Annotated
from pydantic import PastDate
from src.models.expenses import ExpenseRangeType,ExpenseIn
from src.services.expenses import ExpenseServices
from src.db.db import get_db
from src.api.deps import CurrentUser
router = APIRouter(tags=["expenses"],prefix="/expenses")

def get_expense_service():
    return ExpenseServices(session=get_db())

@router.post("/")
def create_expense(
    expense_in:ExpenseIn,
    current_user:CurrentUser,
    service:ExpenseServices = Depends(get_expense_service)
):
    expense = service.create_expense(**expense_in.__dict__,user_id=current_user) #SOLO POR AHORA SERÁ user_id=1
    if expense is None:
        raise HTTPException(
            status_code=422,
            detail="La categoria no existe."
        )
    return expense

@router.get("/")
def get_expenses(
    date_range: ExpenseRangeType,
    current_user:CurrentUser,
    start_date: Annotated[PastDate | None,Query(description='Necesario si date_range es custom')] = None,
    end_date: Annotated[PastDate | None, Query(description='Necesario si date_range es custom')] = None,
    service:ExpenseServices = Depends(get_expense_service)
):
    if date_range == ExpenseRangeType.CUSTOM and (start_date is None or end_date is None):
        raise HTTPException(
            status_code=400,
            detail='La opción custom debe tener start_date y end_date'
        )
    return service.get_expenses(date_range,start_date,end_date,current_user_id=current_user)