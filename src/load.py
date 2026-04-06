import logging
import pandas as pd

from utils import db, db_user, db_pass
        
def load_crypto_price_data(fileName, tableName):
    df = pd.read_csv(f"data/processed/{fileName}/processed.csv")
    
    df.to_sql(tableName, f'postgresql+psycopg2://{db_user}:{db_pass}@localhost:5432/{db}', if_exists='append', index=False)
    
    logging.info('Data loaded successfully!')

def load_coin_data(fileName, tableName):
    df = pd.read_csv(f'data/processed/{fileName}/processed.csv')
    
    df.to_sql(tableName, f'postgresql+psycopg2://{db_user}:{db_pass}@localhost:5432/{db}', if_exists='append', index=False)
    
    logging.info('Data loaded successfully!')
    
if __name__ == "__main__":
    load_crypto_price_data('crypto_price', 'crypto_prices')
    load_coin_data('coin_data', 'crypto_coins')