# Brazilian E-Commerce Data Pipeline

An end-to-end batch data pipeline on the Olist e-commerce dataset. Python loads the order data and daily BRL → EUR exchange rates into PostgreSQL, with dbt transformations and Airflow orchestration to follow. Everything runs in Docker.

## Status

| Phase | Status |
| --- | --- |
| 1. Setup: Docker, PostgreSQL | Done |
| 2. Ingestion: 9 CSVs + exchange rates → `raw` schema | Done |
| 3. Transformation: dbt models and tests | Next |
| 4. Orchestration: Airflow | Planned |

## Tech stack

- **Python 3.13**: pandas and SQLAlchemy for the CSV loads, requests for the API
- **PostgreSQL 16**: data warehouse
- **Docker and Docker Compose**: run the database and the Python jobs
- **Frankfurter API**: daily European Central Bank exchange rates (free, no API key)
- **dbt** and **Airflow**: planned

## How it works
<img width="822" height="437" alt="image" src="https://github.com/user-attachments/assets/ed3e5cd6-b8b1-4d53-9474-0942759b64f6" />


**CSV loader (`load_raw.py`)**
- Every CSV is loaded **as text** (`dtype=str`), so the raw layer keeps values exactly as they arrived, for example zip codes with leading zeros (`01151`). Types are converted later, in the transformation step.
- **Idempotent by replacement:** each run replaces the tables, so rerunning never duplicates rows.

**Exchange-rate loader (`load_exchange_rates.py`)**
- Calls the Frankfurter API for daily BRL → EUR rates for 2016–2018, the period of the orders, and reshapes the JSON into one row per date.
- **Typed table with a primary key** on date and currency pair; the rate is stored as `NUMERIC(12, 6)`, an exact decimal.
- **Idempotent by upsert:** `INSERT ... ON CONFLICT DO UPDATE` updates existing dates instead of duplicating them, so the table can grow without being replaced.
- The European Central Bank publishes no rates on weekends or holidays. Weekend orders will use the most recent earlier rate, handled in dbt.

**Shared connection (`db.py`)**
- One `get_engine()` function builds the database connection from `.env`, and every script imports it.

## Data

The order data is the [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce): about 100k orders from 2016 to 2018, in 9 CSV files. It is not included in this repo. Exchange rates come from the [Frankfurter API](https://frankfurter.dev/), which republishes European Central Bank reference rates.

| Table in `raw` | Source | Rows |
| --- | --- | --- |
| customers | olist_customers_dataset.csv | 99,441 |
| geolocation | olist_geolocation_dataset.csv | 1,000,163 |
| order_items | olist_order_items_dataset.csv | 112,650 |
| order_payments | olist_order_payments_dataset.csv | 103,886 |
| order_reviews | olist_order_reviews_dataset.csv | 99,224 |
| orders | olist_orders_dataset.csv | 99,441 |
| products | olist_products_dataset.csv | 32,951 |
| sellers | olist_sellers_dataset.csv | 3,095 |
| category_name | product_category_name_translation.csv | 71 |
| exchange_rates | Frankfurter API (BRL → EUR, 2016–2018) | 768 |

## How to run

**Requirements:** Docker Desktop and Git.

1. Clone the repo:
   ```
   git clone https://github.com/Kamen-Ivaylov-Marinov/brazilian-ecommerce-pipeline-by-olist.git
   cd brazilian-ecommerce-pipeline-by-olist
   ```
2. Download the dataset from Kaggle (a free account is required), unzip it, and put the 9 CSV files in `data/raw/`.
3. Create your settings file from the template, then set your own password in `.env`:
   ```
   cp .env.example .env
   ```
   (`cp` works in PowerShell too; in CMD use `copy .env.example .env`.)
4. Start PostgreSQL:
   ```
   docker compose up -d
   ```
5. Build the Python image and load the data:
   ```
   docker compose build loader
   docker compose run --rm loader python ingestion/load_raw.py
   docker compose run --rm loader python ingestion/load_exchange_rates.py
   ```
6. Check the data:
   ```
   docker exec -it olist_postgres psql -U olist -d olist_dw -c "SELECT COUNT(*) FROM raw.orders;"
   ```

The database is available from your computer at `localhost:5433`.

## Project structure

```
├── data/raw/                     # source CSVs (not committed)
├── ingestion/
│   ├── db.py                     # shared get_engine() database connection
│   ├── load_raw.py               # loads the 9 CSVs into the raw schema
│   ├── load_exchange_rates.py    # loads BRL → EUR rates from the Frankfurter API
│   └── test_connection.py        # checks the database connection
├── .env.example                  # settings template (copy to .env)
├── docker-compose.yml            # PostgreSQL + the Python loader service
├── Dockerfile                    # image for the Python jobs
└── requirements.txt              # pinned Python packages
```
