from typing import Annotated
from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from src.models.auth import UserIn, UserOut
from src.services.auth import AuthService
from src.db.db import SessionFactory
router = APIRouter(tags=["Autenticacion"],prefix="/auth")

def get_auth_service():
    return AuthService(session=SessionFactory())


@router.post("/register",response_model=UserOut,status_code=201)
def register(user_in:Annotated[UserIn,Form()],
             service:Annotated[AuthService,Depends(get_auth_service)]):
    return service.register(user_in)

@router.post("/login")
def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],
          service:Annotated[AuthService,Depends(get_auth_service)]):
    return service.login(form_data)