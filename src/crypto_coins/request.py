# src/crypto_coins/request.py

import logging

from src.utils import api_key, fetch_data, ENDPOINTS

# URL
coin_list_url = ENDPOINTS['bitcoin_list']

# ---------------------------
# FETCH
# ---------------------------
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