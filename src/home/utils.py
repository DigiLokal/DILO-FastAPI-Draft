import pandas as pd
from sqlalchemy import create_engine, text

from src.db.connection import DB_URL
from src.home.query import *

def get_all_services_data():
    connection = create_engine(DB_URL).connect()
    query = text(get_all_services_query())
    result = connection.execute(query)
    df = pd.DataFrame(result.fetchall())
    df.columns = result.keys()
    connection.close()

    return {
        'services': df.to_dict(orient='records')
    }

def get_all_influencers_data():
    connection = create_engine(DB_URL).connect()
    query = text(get_all_influencers_query())
    result = connection.execute(query)
    df = pd.DataFrame(result.fetchall())
    df.columns = result.keys()
    connection.close()

    return {
        'influencers': df.to_dict(orient='records')
    }

def get_influencer_services_data(username: str):
    connection = create_engine(DB_URL).connect()
    query = text(get_influencer_services_query(username))
    result = connection.execute(query)

    if result.rowcount == 0:
        connection.close()
        return {
            'services': 'No data found for the username'
        }
    
    df = pd.DataFrame(result.fetchall())
    df.columns = result.keys()
    connection.close()
    return {
        'services': df.to_dict(orient='records')
    }