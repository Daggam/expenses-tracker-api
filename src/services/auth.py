from sqlalchemy.orm import Session

from src.core.exceptions import BaseAPIException
from src.db.users import User
from src.models.auth import UserIn
from src.core.security import get_password_hash

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