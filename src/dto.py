from pydantic import BaseModel
from typing import Union

class UserLoginDTO(BaseModel):
    username: str
    password: str

class UserRegisterDTO(BaseModel):
    username: str
    email: str
    password: str
    password_check: str

class ModelInferenceDTO(BaseModel):
    liked_user: list

class DiloUser:
    def __init__(self, username):
        self.username = username