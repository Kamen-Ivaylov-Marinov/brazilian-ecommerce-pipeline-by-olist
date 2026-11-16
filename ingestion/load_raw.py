import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# 1. Connect
# Load the variables from .env
load_dotenv()

# Read the five settings into variables
#    The five are: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
database = os.getenv("POSTGRES_DB")

# Build the connection URL in this format:
url = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"

# Create the engine
engine = create_engine(url)

# 2. Create a schema called "raw" if it doesn't exist
with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))

# 3. Read the CSV into a DataFrame
df = pd.read_csv("data/raw/olist_customers_dataset.csv", dtype=str)

# 4. Write the DataFrame to the table raw.customers
df.to_sql("customers", engine, schema="raw", if_exists="replace", index=False)

# 5. Print how many rows were loaded
print(len(df))