from fastapi.testclient import TestClient
import pytest
from src.main import app
from src.services.expenses import ExpenseServices
from src.api.V1.expenses import get_expense_service


@pytest.fixture
def client(db_session):
    def override_get_expense_service():
        return ExpenseServices(session=db_session)
    app.dependency_overrides[get_expense_service] = override_get_expense_service

    with TestClient(app) as c:
        yield c

def test_create_expense(client):
    response = client.post('/api/v1/expenses/',json={"name": "Expensa 1","category": "Prueba1"})
    assert response.status_code == 200
    created_expense = response.json()
    assert created_expense is not None
    assert created_expense['name'] == "Expensa 1"

def test_error_create_expense(client):
    response = client.post('/api/v1/expenses/',json={"name": "Expensa 1","category": "Prueba"})
    assert response.status_code == 404

def test_get_expenses(client,create_expense):
    response = client.get("/api/v1/expenses/?date_range=past_week")
    assert response.status_code == 200
    expenses = response.json()
    assert expenses is not None
    assert len(expenses) == 3

@pytest.mark.parametrize(("id_expense","status_code"),[(1,200),(99,404)])
def test_delete_expense(client,create_expense,id_expense,status_code):
    response = client.delete(f"/api/v1/expenses/{id_expense}")
    assert response.status_code == status_code
    response = client.get("/api/v1/expenses/?date_range=past_week")
    assert response.status_code == 200
    expenses = response.json()
    assert len(expenses) == (2 if status_code == 200 else 3)

#Actualización de expensas
@pytest.mark.parametrize(("id_expense"),[(1),(2),(3)])
def test_update_expense(client,create_expense,id_expense):
    response = client.patch(f"/api/v1/expenses/{id_expense}",json={"name":"hola","category":"Prueba1"})
    assert response.status_code == 200

