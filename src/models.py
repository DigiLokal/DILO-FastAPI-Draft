from pydantic import BaseModel
from typing import Union

class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    password_check: str