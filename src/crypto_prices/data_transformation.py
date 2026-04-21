# src/crypto_prices/data_transformation.py

import logging
import pandas as pd

from src.extraction import current_time

# Gobal
logging.basicConfig(level=logging.INFO)

# ---------------------------
# TRANSFORMER
# ---------------------------
def transform_crypto_price_data(data):
    if data is None:
        logging.error('No data to transform.')
        return
    
    records = []
    
    try:
        for x, y in data.items():
            records.append({
                "coin_id": x,
                "price_usd": y['usd']
            })
            
        df = pd.DataFrame(records)
        df["timestamp"] = current_time
        
        return df
    except Exception as e:
        logging.error(f"Error occured: {e}")