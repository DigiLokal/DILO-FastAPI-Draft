from sqlalchemy import create_engine

DB_USER = 'postgres'
DB_PASS = 'root123'
DB_HOST = '34.101.46.145'
DB_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}'

def connect_db_test():
    engine = create_engine(DB_URL)

    try:
        connection = engine.connect()
        connection.close()
        return "Connection successful!"
    except Exception as e:
        return f"Connection failed: {e}"