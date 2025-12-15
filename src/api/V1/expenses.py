from datetime import date
from fastapi import APIRouter, Depends, Query
from typing import Annotated, List
from src.models.expenses import ExpenseOut, ExpenseRangeType,ExpenseIn, ExpenseUpdate
from src.services.expenses import ExpenseServices
from src.db.db import SessionFactory
from src.api.deps import CurrentUser
router = APIRouter(tags=["expenses"],prefix="/expenses")

def get_expense_service():
    return ExpenseServices(session=SessionFactory())

@router.post("/",response_model=ExpenseOut)
def create_expense(
    expense_in:ExpenseIn,
    current_user:CurrentUser,
    service:ExpenseServices = Depends(get_expense_service)
):
    expense = service.create_expense(expense_in,user_id=current_user) #SOLO POR AHORA SERÁ user_id=1
    return expense

@router.get("/",response_model=List[ExpenseOut])
def get_expenses(
    date_range: ExpenseRangeType,
    current_user:CurrentUser,
    start_date: Annotated[date | None,Query(description='Necesario si date_range es custom')] = None,
    end_date: Annotated[date | None, Query(description='Necesario si date_range es custom')] = None,
    service:ExpenseServices = Depends(get_expense_service)
):
    return service.get_expenses(date_range,current_user,start_date,end_date)

@router.delete("/{expense_id}",status_code=204)
def delete_expense(
    expense_id:int,
    current_user:CurrentUser,
    service:ExpenseServices = Depends(get_expense_service),
):
    is_deleted = service.delete_expense(expense_id,current_user)
    return 

@router.patch("/{expense_id}",response_model=ExpenseOut)
def update_expense(
    expense_id:int,
    expense_in:ExpenseUpdate,
    current_user:CurrentUser,
    service:ExpenseServices = Depends(get_expense_service)
):
    expense = service.update_expense(expense_id,expense_in,current_user)
    return expense