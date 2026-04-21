import json
import logging
import pandas as pd

from src.utils import PATHS
from src.crypto_coins import fetch_dim_coin_data
from src.crypto_prices import fetch_fact_crypto_prices_data

# Gobal
logging.basicConfig(level=logging.INFO)

# Timestamp
time_format = "%Y%m%d_%H%M%S"
current_time = pd.Timestamp.now()
formatted_current_time = current_time.strftime("%Y%m%d_%H%M%S")

def save_raw_dataset(data, dataset_name):
    if data is None:
        logging.warning("No data to save.")
        return
    
    try:
        # Create dataset-specific folder
        dir_path = PATHS['raw'] / dataset_name
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # File path
        file_path = dir_path / f"{dataset_name}_{formatted_current_time}.json"
        
        with open(file_path, 'w') as f:
            json.dump(data, f)
        
        logging.info(f"{dataset_name} raw data saved successfully!")
        
    except Exception as e:
        logging.error(f"Error occured: {e}")


if __name__ == "__main__":
    crypto_data = fetch_fact_crypto_prices_data()
    save_raw_dataset(crypto_data, "crypto_price")
    
    coin_data = fetch_dim_coin_data()
    save_raw_dataset(coin_data, "coin_data")