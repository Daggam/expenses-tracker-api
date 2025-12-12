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

def test_get_expenses(client,create_expense):
    response = client.get("/api/v1/expenses/?date_range=past_week")
    assert response.status_code == 200
    expenses = response.json()
    assert expenses is not None
    assert len(expenses) == 3
