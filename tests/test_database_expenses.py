from src.models.expenses import Expense,ExpenseCategory
import datetime
import pytest

from tests.conftest import Session

# @pytest.fixture
# def add_categpru(db_session:Session):
#     expense = Expense(1,"Hola")
#     db_session.add(expense)
#     db_session.commit()
#     return expense
    

def test_add_expense(db_session:Session):
    category = ExpenseCategory(id=1,category="Prueba")
    category.expenses.append(Expense(id=1,name='Expensa 1'))
    category.expenses.append(Expense(id=2,name='Expensa 2'))
    category.expenses.append(Expense(id=3,name='Expensa 3'))

    db_session.add(category)
    db_session.commit()
    assert category.category == "Prueba"
    assert len(category.expenses) == 3
    assert category.expenses[0].name == 'Expensa 1'