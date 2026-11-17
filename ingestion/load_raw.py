import pandas as pd
from sqlalchemy import text
from db import get_engine

# Create the engine
engine = get_engine()

# Create a schema called "raw" if it doesn't exist
with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))

files = {"olist_customers_dataset.csv": "customers",
         "olist_geolocation_dataset.csv": "geolocation",
         "olist_order_items_dataset.csv": "order_items",
         "olist_order_payments_dataset.csv": "order_payments",
         "olist_order_reviews_dataset.csv": "order_reviews",
         "olist_orders_dataset.csv": "orders",
         "olist_products_dataset.csv": "products",
         "olist_sellers_dataset.csv": "sellers",
         "product_category_name_translation.csv": "category_name"}

for file_name, table_name in files.items():
    # Read the CSV into a DataFrame
    cur_df = pd.read_csv(f"data/raw/{file_name}", dtype=str)
    
    # Write the DataFrame to the table raw.table_name
    cur_df.to_sql(f"{table_name}", engine, schema= "raw",
                  if_exists= "replace", index=False)
    
    # Print how many rows were loaded
    print(f"{table_name}: {len(cur_df)} rows")
    

