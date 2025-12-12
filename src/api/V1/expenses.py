from fastapi import APIRouter, Depends, Query,HTTPException
from typing import Annotated
from pydantic import PastDate
from src.models.expenses import ExpenseRangeType,ExpenseIn
from src.services.expenses import ExpenseServices
from src.db.db import get_db

router = APIRouter(tags=["expenses"],prefix="/expenses")

def get_expense_service():
    return ExpenseServices(session=get_db())

@router.post("/")
def create_expense(
    expense_in:ExpenseIn,
    service:ExpenseServices = Depends(get_expense_service)
):

    return service.create_expense(**expense_in.__dict__,user_id=1) #SOLO POR AHORA SERÁ user_id=1

@router.get("/")
def get_expenses(
    date_range: ExpenseRangeType,
    start_date: Annotated[PastDate | None,Query(description='Necesario si date_range es custom')] = None,
    end_date: Annotated[PastDate | None, Query(description='Necesario si date_range es custom')] = None,
    service:ExpenseServices = Depends(get_expense_service)
):
    if date_range == ExpenseRangeType.CUSTOM and (start_date is None or end_date is None):
        raise HTTPException(
            status_code=400,
            detail='La opción custom debe tener start_date y end_date'
        )
    return service.get_expenses(date_range,start_date,end_date)