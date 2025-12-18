from datetime import datetime, timedelta, timezone
import bcrypt
from jose import jwt
from src.core.config import settings

def get_password_hash(password:str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(),salt).decode()

def verify_password(password:str,hash:str) -> bool:
    return bcrypt.checkpw(password.encode(),hash.encode())

def create_access_token(data:dict,expires_delta:timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc)
    if expires_delta:
        expire += expires_delta
    else:
        expire += timedelta(minutes=15)
    
    to_encode["exp"] = expire
    encoded_jwt  = jwt.encode(to_encode,settings.SECRET_KEY,settings.ALG_JWT)
    return encoded_jwt