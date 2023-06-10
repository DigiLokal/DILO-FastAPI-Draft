import pandas as pd
from sqlalchemy import create_engine, text

from src.db.connection import DB_URL
from src.profile.query import *

def edit_profile(
        username: str, 
        nama: str = '',
        detail: str = ''
):
    connection = create_engine(DB_URL).connect()
    query = text(edit_profile_query(username, nama, detail))
    connection.execute(query)
    connection.commit()

    return {
        'message': 'Edit success!'
    }

def get_profile_data(username: str):
    connection = create_engine(DB_URL).connect()
    query = text(get_profile_query(username))
    result = connection.execute(query)
    
    df = pd.DataFrame(result.fetchall())
    df.columns = result.keys()
    connection.close()
    return {
        'message': df.to_dict(orient='records')
    }