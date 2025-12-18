from pydantic import BaseModel, ConfigDict,EmailStr, field_validator
import re


class UserIn(BaseModel):
    username:str
    email:EmailStr
    password:str

    @field_validator("password")
    @classmethod
    def password_check(cls,value:str):
        if len(value) < 8:
            raise ValueError("Password must be 8 characters or longer.")
        if not re.search(r"[a-z]",value):
            raise ValueError("Password must contain at least 1 letter.")
        if not re.search(r"[A-Z]",value):
            raise ValueError("Password must contain at least 1 uppercase letter")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]',value):
            raise ValueError("Password must contain at least one special character.")
        return value

class UserOut(BaseModel):
    id:int
    username:str
    email:str

    model_config = ConfigDict(from_attributes=True)

class TokenOut(BaseModel):
    access_token:str
    token_type:str