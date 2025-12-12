import pytest
from src.db.expenses import Expense, ExpenseCategory
from src.db.users import User

def test_usuario(db_session):
    usuarios = db_session.query(User).all()
    assert len(usuarios) == 2
    assert usuarios[0].id == 1
    assert usuarios[0].username == "daggam"

@pytest.mark.parametrize(("id_cat","categoria"),[
    (0,"Prueba1"),
    (1,"Prueba2"),
    (2,"Prueba3")
])
def test_categories(db_session,id_cat,categoria):
    categorias = db_session.query(ExpenseCategory).all()
    assert len(categorias) == 3
    assert categorias[id_cat].category == categoria

def test_create_expense(create_expense,db_session):
    expenses = db_session.query(Expense).all()
    assert len(expenses) == 4
    assert expenses[0].name == "Expensa 1 U1"
    assert expenses[0].user.username == "daggam"
    assert expenses[0].expense_category.category == "Prueba1"