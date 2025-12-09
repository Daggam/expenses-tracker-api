from src.db.expenses import Expense,ExpenseCategory
from src.db.users import User
import datetime
import pytest

from tests.conftest import Session

@pytest.fixture
def add_user(db_session:Session):
    user = User(username='daggam',email='benjaminvilla409@gmail.com',password_hash='adfjd')
    db_session.add(user)
    return user

def test_add_expense(db_session:Session,add_user):
    #Primero se crea la categoria a la cual pertenecen las expensas
    category = ExpenseCategory(category="Prueba")
    my_expenses = [Expense(name='Expensa 1'),
                   Expense(name='Expensa 2'),
                   Expense(name='Expensa 3')
                   ]
    #Luego el usuario crea las expensas (Las expensas dependen de la categoria y del usuario)
    add_user.expenses = my_expenses
    category.expenses = my_expenses

    db_session.add(category)
    db_session.commit()
    assert category.category == "Prueba"
    assert len(category.expenses) == 3
    assert category.expenses[0].name == 'Expensa 1'

def test_add_user(db_session:Session):
    user = User(username='Pruebin',email='pruebin@gmail.com',password_hash='adfjd')
    db_session.add(user)
    db_session.commit()
    assert user.username == 'Pruebin'
    assert len(user.expenses) == 0

