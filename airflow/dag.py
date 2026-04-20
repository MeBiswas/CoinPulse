
from airflow import DAG
from datetime import datetime
from src.load import load_data
from airflow.operators.python import PythonOperator
from extraction import fetch_data, save_raw_dataset
from src.transformation import transform_data, load_latest_file

def pipeline():
    data = fetch_data()
    save_raw_dataset(data)
    df = transform_data(data)
    df.to_csv("data/processed/processed.csv", index=False)
    load_data()

with DAG(
    "crypto_pipeline",
    start_date = datetime(2026, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:
    
    task = PythonOperator(
        task_id="run_pipeline",
        python_callable=pipeline
    )