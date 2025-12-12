from datetime import date,timedelta
from typing import List
from pydantic import PastDate
from sqlalchemy.orm import Session
from src.db.expenses import Expense,ExpenseCategory
from src.db.users import User
from src.models.expenses import ExpenseRangeType

class ExpenseServices:
    def __init__(self, session:Session):
        self._db = session
    
    def get_expenses(self,range_type:ExpenseRangeType,start_date:PastDate | None, end_date:PastDate | None) -> List[Expense]:
        today = date.today()
        match range_type:
            case ExpenseRangeType.PAST_WEEK:
                end_date = today - timedelta(days=7)
            case ExpenseRangeType.PAST_MONTH:
                end_date = today - timedelta(days=30)
            case ExpenseRangeType.LAST_THREE_MONTHS:
                end_date = today - timedelta(days=90)
            #Podría hacer un chequeo si start date <= end_date
        # Pues cuando utilizamos date.today nos da como día YY-mm-dd 00:00:00, y a la base de datos no le sirve mucho, es como si estuviesemos checando ayer.
        today+= timedelta(days=1)
        expenses = self._db.query(Expense).filter(Expense.createAt <= (start_date or today), Expense.createAt >= end_date).all() #Peligroso si me preguntas (Por el start_date or today)
        return expenses

    def create_expense(self,name:str,category:str,user_id:int) -> Expense | None:
        expense_category = self._db.query(ExpenseCategory).filter(ExpenseCategory.category == category).first()
        user = self._db.query(User).filter(User.id == user_id).first()
        if expense_category is None or user is None:
            return None

        expense = Expense(name=name)
        expense.expense_category = expense_category
        expense.user = user
        self._db.add(expense)
        self._db.commit()
        self._db.refresh(expense)
        return expense        


