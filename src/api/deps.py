from typing import Annotated

from jose import jwt
from jose.exceptions import JWTError

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.core.config import settings
from src.db.db import DbSession
from src.db.users import User
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_current_user(db_session:DbSession,
        token:Annotated[str,Depends(oauth2_scheme)]) -> int:
    credential_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )


    try:
        payload = jwt.decode(token,settings.SECRET_KEY,settings.ALG_JWT)
        if "sub" not in payload:
            raise credential_exception
        user=db_session.query(User).filter_by(id=int(payload["sub"])).one_or_none()
        if user is None:
            raise credential_exception
        return user.id
    except JWTError:
        raise credential_exception

CurrentUser = Annotated[int,Depends(get_current_user)]