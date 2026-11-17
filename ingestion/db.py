import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

def get_engine():
    # 1. Load .env
    load_dotenv()
    
    # 2. Read the 5 settings
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    database = os.getenv("POSTGRES_DB")
    
    # 3. Build the url
    url = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"
    
    # 4. Create the engine and RETURN it
    engine = create_engine(url)
    return engine

