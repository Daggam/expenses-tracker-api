from fastapi import APIRouter, Depends, Query,HTTPException
from typing import Annotated
from pydantic import PastDate
from src.models.expenses import ExpenseRangeType,ExpenseIn, ExpenseUpdate
from src.services.expenses import ExpenseServices
from src.db.db import SessionFactory
from src.api.deps import CurrentUser
router = APIRouter(tags=["expenses"],prefix="/expenses")

def get_expense_service():
    return ExpenseServices(session=SessionFactory())

@router.post("/")
def create_expense(
    expense_in:ExpenseIn,
    current_user:CurrentUser,
    service:ExpenseServices = Depends(get_expense_service)
):
    expense = service.create_expense(**expense_in.__dict__,user_id=current_user) #SOLO POR AHORA SERÁ user_id=1
    return expense

@router.get("/")
def get_expenses(
    date_range: ExpenseRangeType,
    current_user:CurrentUser,
    start_date: Annotated[PastDate | None,Query(description='Necesario si date_range es custom')] = None,
    end_date: Annotated[PastDate | None, Query(description='Necesario si date_range es custom')] = None,
    service:ExpenseServices = Depends(get_expense_service)
):
    return service.get_expenses(date_range,start_date,end_date,current_user_id=current_user)

@router.delete("/{expense_id}")
def delete_expense(
    expense_id:int,
    current_user:CurrentUser,
    service:ExpenseServices = Depends(get_expense_service),
):
    is_deleted = service.delete_expense(expense_id,current_user)
    return 

@router.patch("/{expense_id}")
def update_expense(
    expense_id:int,
    expense_in:ExpenseUpdate,
    current_user:CurrentUser,
    service:ExpenseServices = Depends(get_expense_service)
):
    expense = service.update_expense(expense_id,expense_in,current_user)
    return expense