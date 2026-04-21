import json
import logging

from glob import glob
from src.utils import PATHS
from src.crypto_coins import transform_coin_data
from src.crypto_prices import transform_crypto_price_data

# Gobal
logging.basicConfig(level=logging.INFO)

def load_latest_file(dataset_name):
    if not dataset_name:
        logging.error("Please pass dataset name.")
        return 
    
    try:
        file_list = glob(f"data/raw/{dataset_name}/*.json")
        latest_file = max(file_list)
        
        with open(latest_file, 'r') as f:
            data = json.load(f)
        
        logging.info("Dataset loaded successfully!")
        return data
    except Exception as e:
        logging.error(f"Error occured: {e}")
        

def save_processed(df, dataset_name):
    if df is None:
        logging.error('No dataframe to store')
        return
    
    if not dataset_name:
        logging.error('No dataset name')
        return

    try:
        output_dir = PATHS['processed'] / dataset_name
        output_dir.mkdir(parents=True, exist_ok=True)

        # Output path
        output_path = output_dir / "processed.csv"
        df.to_csv(output_path, index=False)

        logging.info(f"Saved processed data to {output_path}")
        return True

    except Exception as e:
        logging.exception(f"Failed to save processed data: {e}")
        return False

if __name__ == "__main__":
    crypto_data = load_latest_file('crypto_price')
    df = transform_crypto_price_data(crypto_data)
    save_processed(df, 'crypto_price')
    
    coin_data = load_latest_file('coin_data')
    coin_data_df = transform_coin_data(coin_data)
    save_processed(coin_data_df, 'coin_data')