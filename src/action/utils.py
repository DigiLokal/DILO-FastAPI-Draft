import uuid
import pandas as pd
from sqlalchemy import create_engine, text

from src.db.connection import DB_URL
from src.action.query import *

def add_order(
        username: str,
        service_id: str,
):
    id = uuid.uuid4()
    connection = create_engine(DB_URL).connect()
    query = text(
        add_order_query(
            id=id,
            username=username,
            service_id=service_id
        )
    )
    connection.execute(query)
    connection.commit()
    connection.close()

    return {
        'message': f'Add order success. Order ID: {id}'
    }

def likes_user(
        username: str,
        likes_user: str,
):
    connection = create_engine(DB_URL).connect()
    query = text(
        add_like_query(
            username=username,
            likes_user=likes_user
        )
    )
    connection.execute(query)
    connection.commit()
    connection.close()

    return {
        'message': 'Added to liked influencers!'
    }

def get_order_data(
        username: str
):
    connection = create_engine(DB_URL).connect()
    query = text(get_order_query(username=username))
    result = connection.execute(query)
    df = pd.DataFrame(result.fetchall())
    df.columns = result.keys()
    connection.close()

    return {
        'message': df.to_dict(orient='records')
    }

def get_likes_data(
        username: str
):
    connection = create_engine(DB_URL).connect()
    query = text(get_likes_query(username=username))
    result = connection.execute(query)
    df = pd.DataFrame(result.fetchall())
    df.columns = result.keys()
    connection.close()

    return {
        'message': df.to_dict(orient='records')
    }