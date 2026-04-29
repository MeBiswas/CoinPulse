import sys, logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.utils.context import Context
from airflow.operators.python import PythonOperator

# Add src to path for imports
sys.path.insert(0, '/opt/airflow')

from src.load import (
    initialize_schema,
    load_data_to_postgres
)
from src.extraction import (
    save_raw_dataset,
    fetch_dim_coin_data,
    fetch_fact_crypto_prices_data
)
from src.transformation import (
    save_processed,
    load_latest_file, 
    transform_coin_data, 
    transform_crypto_price_data
)

# Configure logging
logger = logging.getLogger(__name__)

# =====================
# DAG CONFIGURATION
# =====================
default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['admin@coinpulse.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='coinpulse_etl_pipeline',
    default_args=default_args,
    description='ETL pipeline for CoinPulse - Extract, Transform, and Load crypto data',
    schedule_interval='@daily',
    catchup=False,
    tags=['crypto', 'etl', 'coinpulse'],
)

# =====================
# EXTRACTION TASKS
# =====================
def extract_crypto_data(**context):
    """Extract crypto price data from CoinGecko API and save to raw data directory."""
    try:
        logger.info("Starting extraction of crypto price data...")
        crypto_data = fetch_fact_crypto_prices_data()
        save_raw_dataset(crypto_data, "crypto_price")
        logger.info("Crypto price data extracted successfully")
        context['task_instance'].xcom_push(key='crypto_extracted', value=True)
    except Exception as e:
        logger.error(f"Error extracting crypto data: {e}")
        raise

def extract_coin_data(**context):
    """Extract coin dimension data from CoinGecko API and save to raw data directory."""
    try:
        logger.info("Starting extraction of coin data...")
        coin_data = fetch_dim_coin_data()
        save_raw_dataset(coin_data, "coin_data")
        logger.info("Coin data extracted successfully")
        context['task_instance'].xcom_push(key='coins_extracted', value=True)
    except Exception as e:
        logger.error(f"Error extracting coin data: {e}")
        raise

# =====================
# TRANSFORMATION TASKS
# =====================
def transform_crypto_data(**context):
    """Load latest crypto price raw data and transform it."""
    try:
        logger.info("Starting transformation of crypto price data...")
        crypto_raw_data = load_latest_file('crypto_price')
        crypto_df = transform_crypto_price_data(crypto_raw_data)
        save_processed(crypto_df, 'crypto_price')
        logger.info("Crypto price data transformed successfully")
        context['task_instance'].xcom_push(key='crypto_transformed', value=True)
    except Exception as e:
        logger.error(f"Error transforming crypto data: {e}")
        raise

def transform_coin_data_task(**context):
    """Load latest coin raw data and transform it."""
    try:
        logger.info("Starting transformation of coin data...")
        coin_raw_data = load_latest_file('coin_data')
        coin_df = transform_coin_data(coin_raw_data)
        save_processed(coin_df, 'coin_data')
        logger.info("Coin data transformed successfully")
        context['task_instance'].xcom_push(key='coins_transformed', value=True)
    except Exception as e:
        logger.error(f"Error transforming coin data: {e}")
        raise

# =====================
# LOAD TASKS
# =====================
def initialize_db_schema(**context):
    """Initialize database schema from schema.sql."""
    try:
        logger.info("Initializing database schema...")
        initialize_schema("sql/schema.sql")
        logger.info("Database schema initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing schema: {e}")
        raise

def load_postgres(**context):
    """Load transformed data into PostgreSQL database."""
    try:
        logger.info("Starting data load to PostgreSQL...")
        load_data_to_postgres()
        logger.info("Data loaded to PostgreSQL successfully")
    except Exception as e:
        logger.error(f"Error loading data to PostgreSQL: {e}")
        raise

# =====================
# TASK DEFINITIONS
# =====================
extract_crypto = PythonOperator(
    task_id='extract_crypto_prices',
    python_callable=extract_crypto_data,
    dag=dag,
)

extract_coins = PythonOperator(
    task_id='extract_coin_data',
    python_callable=extract_coin_data,
    dag=dag,
)

transform_crypto = PythonOperator(
    task_id='transform_crypto_prices',
    python_callable=transform_crypto_data,
    dag=dag,
)

transform_coins = PythonOperator(
    task_id='transform_coin_data',
    python_callable=transform_coin_data_task,
    dag=dag,
)

init_schema = PythonOperator(
    task_id='initialize_schema',
    python_callable=initialize_db_schema,
    dag=dag,
)

load_db = PythonOperator(
    task_id='load_to_postgres',
    python_callable=load_postgres,
    dag=dag,
)

# =====================
# DAG DEPENDENCIES
# =====================
extract_crypto >> transform_crypto
extract_coins >> transform_coins

[transform_crypto, transform_coins] >> init_schema >> load_db