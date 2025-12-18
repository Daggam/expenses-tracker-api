from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from src.core.exceptions import BaseAPIException,UserNotFoundError
from src.db.users import User
from src.models.auth import TokenOut, UserIn
from src.core.security import create_access_token, get_password_hash, verify_password
from src.core.config import settings

class AuthService():
    def __init__(self,session:Session):
        self._db = session

    def register(self,user_in:UserIn) -> User:
        #Nos fijamos si ya existe el usuario.
        user = self._db.query(User.id).filter(User.email == user_in.email).one_or_none()
        if user is not None:
            raise BaseAPIException(message="The email has already been registered.")
        
        password_hashed = get_password_hash(user_in.password)

        user = User(username=user_in.username,email=user_in.email,password_hash=password_hashed)
        self._db.add(user)
        self._db.commit()
        return user

    def login(self,form_data:OAuth2PasswordRequestForm) -> TokenOut:
        user = self._db.query(User).filter(User.username == form_data.username).one_or_none()
        print(user)
        if user is None or not verify_password(form_data.password,user.password_hash):
            raise BaseAPIException(message="Username or password incorrect.",status_code=401)
        data = {"sub":str(user.id)}
        access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data,access_token_expire)

        return TokenOut(access_token=access_token,token_type="bearer")