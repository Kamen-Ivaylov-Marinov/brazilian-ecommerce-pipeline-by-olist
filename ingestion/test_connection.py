import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# 1. Load the variables from .env
load_dotenv()

# 2. Read the five settings into variables
#    Hint: os.getenv("POSTGRES_USER")
#    The five are: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
database = os.getenv("POSTGRES_DB")

# 3. Build the connection URL in this format:
#    postgresql+psycopg://USER:PASSWORD@HOST:PORT/DATABASE
#    Hint: an f-string
url = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"

# 4. Create the engine
#    Hint: engine = create_engine(url)
engine = create_engine(url)

# 5. Connect and ask PostgreSQL for its version
#    with engine.connect() as conn:
#        result = conn.execute(text("SELECT version()")).scalar()
#    then print the result
with engine.connect() as conn:
    result = conn.execute(text("SELECT version()")).scalar()
print(result)

