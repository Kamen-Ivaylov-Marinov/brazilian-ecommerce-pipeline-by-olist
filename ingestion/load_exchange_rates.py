import requests
from sqlalchemy import text
from db import get_engine

START_DATE = "2016-01-01"
# If START_DATE has no rate (weekend/holiday), the API starts at the
# previous available date, e.g. 2015-12-31 for a 2016-01-01 start.
END_DATE = "2018-12-31"
BASE = "BRL"
TARGET = "EUR"

URL = f"https://api.frankfurter.dev/v1/{START_DATE}..{END_DATE}?base={BASE}&symbols={TARGET}"

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS raw.exchange_rates (
    rate_date        DATE           NOT NULL,
    base_currency    TEXT           NOT NULL,
    target_currency  TEXT           NOT NULL,
    rate             NUMERIC(12, 6) NOT NULL,
    loaded_at        TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (rate_date, base_currency, target_currency)
)
"""

UPSERT = """
INSERT INTO raw.exchange_rates (rate_date, base_currency, target_currency, rate)
VALUES (:rate_date, :base_currency, :target_currency, :rate)
ON CONFLICT (rate_date, base_currency, target_currency)
DO UPDATE SET rate = EXCLUDED.rate, loaded_at = CURRENT_TIMESTAMP
"""

# 1. Get the engine
engine = get_engine()

# 2. Create the table if it doesn't exist
with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))
    conn.execute(text(CREATE_TABLE))

# 3. Call the API
response = requests.get(URL, timeout=30)
response.raise_for_status()
data = response.json()

# 4. Reshape the JSON into a list of rows (one dict per date)
#    Each row: {"rate_date": ..., "base_currency": "BRL", "target_currency": "EUR", "rate": ...}
rows = []
for rate_date, rate_value in data["rates"].items():
    row = {"rate_date": rate_date, "base_currency": BASE,
           "target_currency": TARGET, "rate": rate_value[TARGET]}
    rows.append(row)
 

# 5. Insert the rows
with engine.begin() as conn:
    conn.execute(text(UPSERT), rows)

# 6. Print how many rows were loaded
print(f"exchange_rates: {len(rows)} rows")