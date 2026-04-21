# src/crypto_coins/transformer.py

import logging
import pandas as pd

# Gobal
logging.basicConfig(level=logging.INFO)

# ---------------------------
# TRANSFORMER
# ---------------------------
def transform_coin_data(data):
    if data is None:
        logging.error('No data to transform')
        return
    
    try:
        df = pd.DataFrame(data)
        new_df = df.loc[:, ['id', 'symbol', 'name']].rename(columns={'id': 'coin_id'})
        return new_df
    except Exception as e:
        logging.error(f"Error occured: {e}")