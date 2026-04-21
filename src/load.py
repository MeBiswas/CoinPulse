import logging
import pandas as pd
from sqlalchemy import text, create_engine

from src.crypto_coins import upsert_coins
from src.crypto_prices import upsert_prices
from src.utils.config import db, db_user, db_pass

# Gobal
logging.basicConfig(level=logging.INFO)
        
def get_engine():
    return create_engine(
        f'postgresql+psycopg2://{db_user}:{db_pass}@localhost:5432/{db}'
    )

def initialize_schema(schema_path="sql/schema.sql"):
    """Reads and executes the schema.sql file to create tables."""
    engine = get_engine()
    try:
        with open(schema_path, 'r') as f:
            sql_commands = f.read()
        
        with engine.connect() as conn:
            conn.execute(text(sql_commands))
            conn.commit()
        logging.info("Schema initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing schema: {e}")
        raise e

# ---------------------------
# MAIN LOAD FUNCTION
# ---------------------------
def load_data_to_postgres():
    engine = get_engine()
    
    """
        1. Loading Coin Data first (Dimension Table)
        This must be first due to Foreign Key constraints
    """
    try:
        coins_df = pd.read_csv('data/processed/coin_data/processed.csv')
        coins_df = coins_df.drop_duplicates(subset=['coin_id'])
        
        upsert_coins(engine, coins_df)
        
        logging.info("Coins dimension table updated.")
    except Exception as e:
        logging.error(f"Error loading coins: {e}")
        raise

    """
        2. Load Price Data (Fact Table)
    """
    try:
        prices_df = pd.read_csv('data/processed/crypto_price/processed.csv')
        prices_df = prices_df.drop_duplicates(subset=['coin_id', 'timestamp'])
        
        upsert_prices(engine, prices_df)
         
        logging.info("Prices fact table updated.")
    except Exception as e:
        logging.error(f"Error loading prices: {e}")
    
if __name__ == "__main__":
    initialize_schema()
    load_data_to_postgres()