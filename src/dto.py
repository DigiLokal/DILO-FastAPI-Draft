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

class ProfileDTO(BaseModel):
    username: str
    nama: Union[str, None] = None
    detail: Union[str, None] = None    

class AddOrderDTO(BaseModel):
    username: str
    service_id: str

class UserLikesDTO(BaseModel):
    username: str
    likes_user: str

class DiloUser:
    def __init__(self, username):
        self.username = username