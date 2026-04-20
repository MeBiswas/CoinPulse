import logging
import pandas as pd
from sqlalchemy import text, create_engine
from src.utils.config import db, db_user, db_pass
        
def get_engine():
    return create_engine(f'postgresql+psycopg2://{db_user}:{db_pass}@localhost:5432/{db}')

def initialize_schema(schema_path="sql/schema.sql"):
    """Reads and executes the schema.sql file to create tables."""
    engine = get_engine()
    try:
        with open(schema_path, 'r') as f:
            sql_commands = f.read()
        
        with engine.connect() as conn:
            # We use text() to tell SQLAlchemy this is a raw SQL string
            conn.execute(text(sql_commands))
            conn.commit()
        logging.info("Schema initialized successfully.")
    except Exception as e:
        logging.error(f"Error initializing schema: {e}")
        raise e
        
def load_data_to_postgres():
    engine = get_engine()
    
    """
        1. Loading Coin Data first (Dimension Table)
        This must be first due to Foreign Key constraints
    """
    try:
        coins_df = pd.read_csv('data/processed/coin_data/processed.csv')
        # Use 'multi' method for better performance with PostgreSQL
        coins_df.to_sql('crypto_coins', engine, if_exists='append', index=False, method='multi')
        logging.info("Coins dimension table updated.")
    except Exception as e:
        logging.error(f"Error loading coins: {e}")

    """
        2. Load Price Data (Fact Table)
    """
    try:
        prices_df = pd.read_csv('data/processed/crypto_price/processed.csv')
        prices_df.to_sql('crypto_prices', engine, if_exists='append', index=False, method='multi')
        logging.info("Prices fact table updated.")
    except Exception as e:
        logging.error(f"Error loading prices: {e}")
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    initialize_schema()
    load_data_to_postgres()