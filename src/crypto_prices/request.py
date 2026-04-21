# src/crypto_prices/request.py

from src.utils import api_key, fetch_data, ENDPOINTS

# URL
crypto_price_url = ENDPOINTS['bitcoin_market_price_data']

# ---------------------------
# FETCH
# ---------------------------
def fetch_fact_crypto_prices_data():
    if not api_key:
        print("Error: API_KEY not found!")
        return 

    # list of IDs
    crypto_list = ['bitcoin', 'ethereum', 'solana', 'dogecoin', 'ripple']
    ids_param = ",".join(crypto_list)
    
    return fetch_data(crypto_price_url, {
        'ids': ids_param,
        'vs_currencies': 'usd',
        'x_cg_demo_api_key': api_key
    })