from fastapi import FastAPI

from .dto import *
from src.db.connection import connect_db_test
from src.auth.utils import *
from src.ml.utils import *
from src.home.utils import *

app = FastAPI()

### Health Check ###
@app.get("/")
async def root():
    return {
        'message': 'Hi! I am DiDO',
        'db_connection_status': connect_db_test()
    }

#-- Auth --#
@app.post("/login")
async def login_endpoint(user_login: UserLoginDTO):
    return login(
        username=user_login.username,
        password=user_login.password
    )

@app.post("/register")
async def register_endpoint(user_register: UserRegisterDTO):
    return register(
        username=user_register.username,
        email=user_register.email,
        password=user_register.password,
        password_check=user_register.password_check
    )

#-- Home --#
@app.get("/home/all-services")
async def get_all_services_endpoint():
    return get_all_services_data()

@app.get("/home/all-influencers")
async def get_all_influencers_endpoint():
    return get_all_influencers_data()

#-- Influencer Specific Page --#
@app.get("/influencer/{username}/available-services")
async def get_influencer_services(username: str):
    return get_influencer_services_data(
        username=username
    )

#-- Machine Learning --#
@app.post("/ml/inference")
async def ml_inference_endpoint(model_inference: ModelInferenceDTO):
    return {
        'message': model_predict(
            user_ids=model_inference.liked_user
        )
    }

@app.post("/ml/training")
async def ml_training_endpoint():
    return {
        'message': 'ML Training'
    }