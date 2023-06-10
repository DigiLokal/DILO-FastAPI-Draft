import hashlib
import uuid
from sqlalchemy import create_engine, text
from fastapi import Depends, FastAPI
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordBearer
import jwt

from .dto import *
from src.db.connection import connect_db_test
from src.auth.utils import register, hash
from src.auth.query import *
from src.ml.utils import *
from src.home.utils import *
from src.profile.utils import *
from src.action.utils import *

app = FastAPI()

SECRET = "dilo-keren"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
manager = LoginManager(SECRET, "/login")

#-- Supporting --#
def get_current_user(token: str = Depends(oauth2_scheme)):
    user = get_user_from_token(token)
    if user:
        return DiloUser(user)

def get_user_from_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload.get('sub')
    except Exception:
        return None

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
    username=str(user_login.username)
    password=str(user_login.password)
    
    connection = create_engine(DB_URL).connect()
    query = text(check_username_exist_query(username=username))
    check_username = connection.execute(query)
    if check_username.fetchone()[0] == 0:
        connection.close()
        return {
            'message': 'Username not found!'
        }
    else:
        query = text(login_query(username, hash(password)))
        result = connection.execute(query)
        if result.fetchone()[0] < 1:
            connection.close()
            return {
                'message': 'Wrong password!'
            }
        else:
            connection.close()
            access_token = manager.create_access_token(
                data={
                    'sub': username
                }
            )

            return {
                'message': 'Login success!',
                'token': access_token
            }

@app.get('/protected_branch')
def protected_branch(user: DiloUser = Depends(get_current_user)):
    return {'message': f'Access to protected branch granted for user: {user.username}'}

@app.post("/register")
async def register_endpoint(user_register: UserRegisterDTO):
    return register(
        username=user_register.username,
        email=user_register.email,
        password=user_register.password,
        password_check=user_register.password_check
    )

#-- Profile --#
@app.put("/profile")
async def edit_profile_endpoint(profile: ProfileDTO):
    return edit_profile(
        username=profile.username,
        nama=profile.nama,
        detail=profile.detail
    )

@app.get("/profile/{username}")
async def get_profile_endpoint(username: str):
    return get_profile_data(
        username=username
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
async def get_influencer_services_endpoint(username: str):
    return get_influencer_services_data(
        username=username
    )

#-- Actions --#
@app.post("/add-order")
async def add_order_endpoint(order: AddOrderDTO):
    return add_order(
        username=order.username,
        service_id=order.service_id
    )

@app.get("/order/{username}")
async def get_order_endpoint(username: str):
    return get_order_data(
        username=username
    )

@app.post("/like")
async def user_likes_endpoint(likes: UserLikesDTO):
    return likes_user(
        username=likes.username,
        likes_user=likes.likes_user
    )

@app.get("/like/{username}")
async def get_likes_endpoint(username: str):
    return get_likes_data(
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