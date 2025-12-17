from fastapi.testclient import TestClient
from src.db.users import User
from src.main import app
from src.api.V1.auth import get_auth_service
from src.services.auth import AuthService
import pytest

@pytest.fixture()
def client(db_session):
    def override_get_auth_service():
        return AuthService(session=db_session)
    
    app.dependency_overrides[get_auth_service] = override_get_auth_service
    
    with TestClient(app) as c:
        yield c

def test_create_user(db_session,client):
    headers = {'Content-Type':"application/x-www-form-urlencoded"}

    data = {
        "username":"Gonza",
        "email":"Gonza@mgmail.com",
        "password":"aA!45678"
        }
    
    response = client.post("/api/v1/auth/register",
                           headers = headers,
                           data=data
                           )
    assert response.status_code == 201
    user = response.json()

    #Me aseguro que esté en la base de datos
    user_db = db_session.query(User).filter(User.id == user["id"]).one_or_none()
    assert not user_db is None
    assert user_db.username == user["username"]
    assert user_db.email == user["email"]

#Después se puede corrobrar si el dominio EXISTE. (Si existe el correo)
@pytest.mark.parametrize("email,password,expected_message",[("email","123456","value is not a valid email address: An email address must have an @-sign."),
                                                            ("email@email.com","123456","Value error, Password must be 8 characters or longer."),
                                                            ("email@email.com","12345678","Value error, Password must contain at least 1 letter."),
                                                            ("email@email.com","a2345678","Value error, Password must contain at least 1 uppercase letter"),
                                                            ("email@email.com","aA345678","Value error, Password must contain at least one special character."),
                                                            ("email@email.com","!A345678","Value error, Password must contain at least 1 letter.")])
def test_create_user_errors(client,email,password,expected_message):
    headers = {'Content-Type':"application/x-www-form-urlencoded"}

    data = {
        "username":"Gonza",
        "email":email,
        "password":password
        }
    response = client.post("/api/v1/auth/register",
                           headers = headers,
                           data=data
                           )
    assert response.status_code == 422

    res = response.json()
    assert res["detail"][0]["msg"] == expected_message