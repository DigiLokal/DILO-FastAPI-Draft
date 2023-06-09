import hashlib
import uuid
from sqlalchemy import create_engine, text

from src.db.connection import DB_URL
from src.auth.query import *

def login(
        username: str, 
        password: str,
        manager
):
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

def register(
        username: str, 
        email: str,
        password: str, 
        password_check: str
):
    if password != password_check:
        return {
            'Password is different!'
        }
    else:
        connection = create_engine(DB_URL).connect()
        query = text(check_username_exist_query(username=username))
        check_username = connection.execute(query)
        if check_username.fetchone()[0] != 0:
            connection.close()
            return {
                'message': 'Username already exist!'
            }
        else:
            user_id = str(uuid.uuid4())

            query = text(get_umkm_count_query())
            umkm_count = int(connection.execute(query).fetchone()[0])

            query = text(register_query(user_id, username, hash(password), email, umkm_count+1))
            connection.execute(query)

            query = text(update_umkm_count_query())
            connection.execute(query)

            connection.commit()
            connection.close()
            return {
                'message': 'Register success!'
            }

def hash(password: str) -> str:
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password
