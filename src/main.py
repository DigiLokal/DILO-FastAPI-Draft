from fastapi import FastAPI
from src.models import UserLogin, UserRegister

app = FastAPI()

@app.get("/")
async def root():
    return {
        'message': 'Hi! I am DiDO'
    }

@app.post("/login")
async def login_template(user_login: UserLogin):
    return user_login

@app.post("/register")
async def register_template(user_register: UserRegister):
    return user_register