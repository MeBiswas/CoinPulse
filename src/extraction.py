import os
import json
import logging

from datetime import datetime
from src.utils import PATHS, api_key, fetch_data, ENDPOINTS

# Gobal
logging.basicConfig(level=logging.INFO)
coin_list_url = ENDPOINTS['bitcoin_list']
crypto_price_url = ENDPOINTS['bitcoin_market_price_data']

def fetch_fact_crypto_prices_data():
    if not api_key:
        print("Error: API_KEY not found!")
        return 
        
    return fetch_data(crypto_price_url, {
        'ids': 'bitcoin',
        'vs_currencies': 'usd',
        'x_cg_demo_api_key': api_key
    })

def fetch_dim_coin_data():
    if not api_key:
        logging.error("Error: API_KEY not found!")
        return
    
    return fetch_data(coin_list_url, {
        "page": 1,
        "per_page": 250,
        "vs_currency": "usd",
        "order": "market_cap_desc"
    })

def save_raw_dataset(data, dataset_name):
    if data is None:
        logging.warning("No data to save.")
        return
    
    try:
        time_format = "%Y%m%d_%H%M%S"
        timestamp = datetime.now().strftime(time_format)
        
        # Create dataset-specific folder
        dir_path = PATHS['raw'] / dataset_name
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # File path
        file_path = dir_path / f"{dataset_name}_{timestamp}.json"
        
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