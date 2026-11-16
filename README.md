# Brazilian E-Commerce Data Pipeline

An end-to-end batch data pipeline on the Olist e-commerce dataset, built with Python, PostgreSQL, dbt and Airflow, all running in Docker.

## Dataset

This project uses the [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
(about 100k orders from 2016 to 2018, in 9 CSV files).

The data is not included in this repo. To run the project:

1. Download the dataset from Kaggle (a free account is required).
2. Unzip it and put the 9 CSV files in `data/raw/`.