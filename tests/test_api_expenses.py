from datetime import date, timedelta
from fastapi.testclient import TestClient
import pytest
from src.main import app
from src.services.expenses import ExpenseServices
from src.api.V1.expenses import get_expense_service
from src.core.exceptions import BaseAPIException

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

#1. Verificar que le pertenece al usuario actual?
@pytest.mark.parametrize("date_range, expected_length",[("past_week",6),
                                                         ("past_month",9),
                                                         ("past_three_months",12)
                                                        ])
def test_get_expenses(client,create_expenses_datetimes,date_range,expected_length):
    response = client.get(f"/api/v1/expenses/?date_range={date_range}")
    assert response.status_code == 200
    expenses = response.json()
    assert expenses is not None
    assert len(expenses) == expected_length

#TODO:
# 1- Un test que vea los casos borde de custom.
# 2- Un test que vea todos que compruebe que todos los errores son ejecutados:
#                           a. start_date > end_date
#                           b. custom pero con start_date null y/o end_date null (todas las combinaciones)
#                           c. No custom pero con start_date no null y/o end_date no null
#                           d. custom pero con start_date > today y/o end_date > today
# 
@pytest.mark.parametrize("start_date, end_date, expected_value", [(date.today(),date.today(),3),
                                                                  (date.today() - timedelta(days=7),date.today(),6),
                                                                  (date.today() - timedelta(days=40),date.today() - timedelta(days=7),6)])
def test_get_expenses_custom(client,create_expenses_datetimes,start_date,end_date,expected_value):
    response = client.get(f"/api/v1/expenses",
                          params={
                                    "date_range":"custom",
                                    "start_date":start_date,
                                    "end_date":end_date
                                })
    assert response.status_code == 200
    expenses = response.json()
    assert len(expenses) == expected_value



@pytest.mark.parametrize("start_date, end_date, error_message",[(None,None,"Custom option should have start_date and end_date"),
                                                                (None,date.today(),"Custom option should have start_date and end_date"),
                                                                (date.today(),None,"Custom option should have start_date and end_date"),
                                                                (date.today(),date.today() + timedelta(days=7),"start_date/end_date should be lesser or equal than today"),
                                                                (date(2020,2,1),date(2020,1,1),"end_date should be greater or equal than start_date")])
def test_get_expenses_custom_error(client,start_date,end_date,error_message):
    prms = {"date_range":"custom"}
    if start_date is not None:
        prms["start_date"] = start_date
    if end_date is not None:
        prms["end_date"] = end_date
    
    response = client.get("/api/v1/expenses",params=prms)
    assert response.status_code == 422
    msg = response.json()
    assert msg["message"] == error_message

@pytest.mark.parametrize("range_type, start_date, end_date",[("past_week",date.today(),date.today()),
                                                             ("past_week",None,date.today()),
                                                             ("past_week",date.today(),None),
                                                             ])
def test_get_expenses_non_custom_error(client,range_type,start_date,end_date):
    prms = {"date_range":range_type}
    if start_date is not None:
        prms["start_date"] = start_date
    if end_date is not None:
        prms["end_date"] = end_date
    
    response = client.get("/api/v1/expenses",params=prms)
    assert response.status_code == 422
    msg = response.json()
    assert msg["message"] == "start_date and end_date filter is only available when custom option is setted."

@pytest.mark.parametrize(("id_expense","status_code"),[(1,204),(99,404)])
def test_delete_expense(client,create_expense,id_expense,status_code):
    response = client.delete(f"/api/v1/expenses/{id_expense}")
    assert response.status_code == status_code
    response = client.get("/api/v1/expenses/?date_range=past_week")
    assert response.status_code == 200
    expenses = response.json()
    assert len(expenses) == (2 if status_code == 204 else 3)

#Actualización de expensas
@pytest.mark.parametrize(("id_expense"),[(1),(2),(3)])
def test_update_expense(client,create_expense,id_expense):
    response = client.patch(f"/api/v1/expenses/{id_expense}",json={"name":"hola","category":"Prueba1"})
    assert response.status_code == 200

