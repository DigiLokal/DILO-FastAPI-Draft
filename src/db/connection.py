from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv('../.env')

DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}'

def connect_db_test():
    engine = create_engine(DB_URL)

    try:
        connection = engine.connect()
        connection.close()
        return "Connection successful!"
    except Exception as e:
        return f"Connection failed: {e}"