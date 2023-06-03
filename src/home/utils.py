import pandas as pd
from sqlalchemy import create_engine, text

from src.db.connection import DB_URL
from src.home.query import get_all_services, get_all_influencers, get_influencer_services

def get_all_services_data():
    connection = create_engine(DB_URL).connect()
    query = text(get_all_services())
    result = connection.execute(query)
    df = pd.DataFrame(result.fetchall())
    df.columns = result.keys()
    connection.close()

    return {
        'message': df.to_dict(orient='records')
    }

def get_all_influencers_data():
    connection = create_engine(DB_URL).connect()
    query = text(get_all_influencers())
    result = connection.execute(query)
    df = pd.DataFrame(result.fetchall())
    df.columns = result.keys()
    connection.close()

    return {
        'message': df.to_dict(orient='records')
    }

def get_influencer_services_data(username: str):
    connection = create_engine(DB_URL).connect()
    query = text(get_influencer_services(username))
    result = connection.execute(query)

    if result.rowcount == 0:
        connection.close()
        return {
            'message': 'No data found for the username'
        }
    
    df = pd.DataFrame(result.fetchall())
    df.columns = result.keys()
    connection.close()
    return {
        'message': df.to_dict(orient='records')
    }