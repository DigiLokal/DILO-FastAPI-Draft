import hashlib
import uuid
from sqlalchemy import create_engine, text

from src.db.connection import DB_URL
from src.auth.query import register_query, login_query, check_username_exist

def login(
        username: str, 
        password: str
):
    connection = create_engine(DB_URL).connect()
    query = text(check_username_exist(username=username))
    check_username = connection.execute(query)
    if check_username.fetchone()[0] == 0:
        connection.close()
        return 'Username not found!'
    else:
        query = text(login_query(username, hash(password)))
        result = connection.execute(query)
        if result.fetchone()[0] < 1:
            connection.close()
            return 'Wrong password!'
        else:
            connection.close()
            return 'Login success!'

def register(
        username: str, 
        email: str,
        password: str, 
        password_check: str
):
    if password != password_check:
        return 'Password is different!'
    else:
        connection = create_engine(DB_URL).connect()
        query = text(check_username_exist(username=username))
        check_username = connection.execute(query)
        if check_username.fetchone()[0] != 0:
            connection.close()
            return 'Username already exist!'
        else:
            user_id = str(uuid.uuid4())
            query = text(register_query(user_id, username, hash(password), email))
            connection.execute(query)
            
            connection.commit()
            connection.close()
            return 'Register success!'

def hash(password: str) -> str:
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password