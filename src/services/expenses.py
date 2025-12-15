from datetime import date, datetime,timedelta, timezone
from typing import List
from sqlalchemy.orm import Session
from src.db.expenses import Expense,ExpenseCategory
from src.db.users import User
from src.models.expenses import ExpenseIn, ExpenseRangeType, ExpenseUpdate
from src.core.exceptions import BaseAPIException,ExpenseCategoryNotFoundError, ExpenseNotFoundError,InvalidModelError
class ExpenseServices:
    def __init__(self, session:Session):
        self._db = session
    
    def get_expenses(self,range_type:ExpenseRangeType,current_user_id:int,start_date:date | None = None, end_date:date | None = None) -> List[Expense]:        
        if range_type == ExpenseRangeType.CUSTOM and (start_date is None or end_date is None):
            raise BaseAPIException(
                message="Custom option should have start_date and end_date",
                status_code=422,
            )
        #start_date y end_date solo puede ser seteados cuando expenseRange es custom.
        if range_type != ExpenseRangeType.CUSTOM and not (start_date is None and end_date is None):
            raise BaseAPIException(
                message="start_date and end_date filter is only available when custom option is setted.",
                status_code=422,
            )
        
        if end_date is None:
            end_date = datetime.now(timezone.utc)
    
        match range_type:
            case ExpenseRangeType.PAST_WEEK:
                start_date = end_date - timedelta(days=7)
            case ExpenseRangeType.PAST_MONTH:
                start_date = end_date - timedelta(days=30)
            case ExpenseRangeType.LAST_THREE_MONTHS:
                start_date = end_date - timedelta(days=90)
            case ExpenseRangeType.CUSTOM:
                today = date.today()
                if start_date > today or end_date > today:
                    raise BaseAPIException(
                        message="start_date/end_date should be lesser or equal than today",
                        status_code=422
                    )
                if start_date > end_date:
                    raise BaseAPIException(
                        message="end_date should be greater or equal than start_date",
                        status_code=422
                    )
                start_date = datetime.combine(start_date,datetime.min.time(),tzinfo=timezone.utc)
                end_date = datetime.combine(end_date,datetime.min.time(),tzinfo=timezone.utc)

        end_date= end_date.replace(hour=0,minute=0,second=0,microsecond=0)
        start_date = start_date.replace(hour=0,minute=0,second=0,microsecond=0)
        # Pues cuando utilizamos date.today nos da como día YY-mm-dd 00:00:00, y a la base de datos no le sirve mucho, es como si estuviesemos checando ayer.
        tomorrow = end_date + timedelta(days=1)
        
        expenses = self._db.query(Expense).filter(Expense.createdAt >= start_date,
                                              Expense.createdAt < tomorrow,
                                              Expense.id_user == current_user_id).all()
        return expenses

    def create_expense(self,expense_in:ExpenseIn,user_id:int) -> Expense | None:
        expense_category = self._db.query(ExpenseCategory).filter(ExpenseCategory.category == expense_in.category).first()
        user = self._db.query(User).filter(User.id == user_id).first()
        if expense_category is None: #or user is None:
            raise ExpenseCategoryNotFoundError(expense_in.category)

        expense = Expense(name=expense_in.name)
        expense.expense_category = expense_category
        expense.user = user
        self._db.add(expense)
        self._db.commit()
        self._db.refresh(expense)
        return expense        

    def delete_expense(self,expense_id:int,user_id:int) -> bool:
        expense = self._db.query(Expense).filter(Expense.id == expense_id,Expense.id_user == user_id).one_or_none()
        if expense is None:
            raise ExpenseNotFoundError(expense_id)
        self._db.delete(expense)
        self._db.commit()
        return True

    def update_expense(self, expense_id:int,expense_in:ExpenseUpdate,user_id:int) -> Expense | None:
        if len(expense_in.model_fields_set) == 0:
            raise InvalidModelError()
        #Tendría que detectar la forma para saber si la expensa le pertenece al usuario actual(es decir, si no lo es, es un http 403)
        expense = self._db.query(Expense).filter(Expense.id == expense_id,Expense.id_user == user_id).one_or_none()
        
        if expense is None:
            raise ExpenseNotFoundError(expense_id)
        #HAY QUE TENER CUIDADO CON LOS NONE's (Por eso lo excluimos)
        update_attr = expense_in.model_dump(exclude_unset=True)

        if "name" in update_attr:
            expense.name = update_attr["name"]
        if "category" in update_attr:
            expense_category = self._db.query(ExpenseCategory).filter(ExpenseCategory.category == update_attr["category"]).one_or_none()
            if expense_category is None:
                raise ExpenseCategoryNotFoundError(update_attr["category"])
            expense.expense_category = expense_category

        self._db.commit()
        return expense