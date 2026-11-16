# Brazilian E-Commerce Data Pipeline

An end-to-end batch data pipeline on the Olist e-commerce dataset. Python loads the source data into PostgreSQL, with dbt transformations and Airflow orchestration to follow. Everything runs in Docker.

## Status

| Phase | Status |
| --- | --- |
| 1. Setup: Docker, PostgreSQL | Done |
| 2. Ingestion: CSVs → `raw` schema | Done |
| 2b. Exchange rates: BRL → EUR from the Frankfurter API | In progress |
| 3. Transformation: dbt models and tests | Planned |
| 4. Orchestration: Airflow | Planned |

## Tech stack

- **Python 3.13** with pandas and SQLAlchemy: ingestion
- **PostgreSQL 16**: data warehouse
- **Docker and Docker Compose**: runs the database and the Python jobs
- **dbt** and **Airflow**: planned

## How it works

```
data/raw/*.csv  →  Python loader (Docker)  →  PostgreSQL: raw schema
```

- Every CSV is loaded **as text** (`dtype=str`), so the raw layer keeps values exactly as they arrived (for example, zip codes with leading zeros). Types are converted later, in the transformation step.
- Loads are **idempotent**: each run replaces the tables, so rerunning never duplicates rows.

## Dataset

This project uses the [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce): about 100k orders from 2016 to 2018, in 9 CSV files. The data is not included in this repo.

| Table in `raw` | Source file | Rows |
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
   (On Windows PowerShell, `cp` works too; in CMD use `copy .env.example .env`.)
4. Start PostgreSQL:
   ```
   docker compose up -d
   ```
5. Build the Python image and load the data:
   ```
   docker compose build loader
   docker compose run --rm loader python ingestion/load_raw.py
   ```
6. Check the data:
   ```
   docker exec -it olist_postgres psql -U olist -d olist_dw -c "SELECT COUNT(*) FROM raw.orders;"
   ```

The database is available from your computer at `localhost:5433`.

## Project structure

```
├── data/raw/              # source CSVs (not committed)
├── ingestion/
│   ├── load_raw.py        # loads the 9 CSVs into the raw schema
│   └── test_connection.py # checks the database connection
├── .env.example           # settings template (copy to .env)
├── docker-compose.yml     # PostgreSQL + the Python loader service
├── Dockerfile             # image for the Python jobs
└── requirements.txt       # pinned Python packages
```
