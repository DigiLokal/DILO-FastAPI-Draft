from fastapi import FastAPI

from .dto import *
from src.db.connection import connect_db_test
from src.auth.utils import register, login

app = FastAPI()

@app.get("/")
async def root():
    return {
        'message': 'Hi! I am DiDO'
    }

@app.post("/login")
async def login_template(user_login: UserLogin):
    return login(
        username=user_login.username,
        password=user_login.password
    )

@app.post("/register")
async def register_template(user_register: UserRegister):
    return register(
        username=user_register.username,
        email=user_register.email,
        password=user_register.password,
        password_check=user_register.password_check
    )

@app.get("/db_connection_test")
async def db_connection_test():
    return connect_db_test()

@app.post("/ml/inference")
async def ml_inference(model_inference: ModelInference):
    return model_inference(
        model_inference.liked_user
    )

@app.post("/ml/training")
async def ml_inference():
    return {
        'message': 'ML Training'
    }