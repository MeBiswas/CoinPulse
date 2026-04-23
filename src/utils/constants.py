# utils/constants.py

from pathlib import Path

BASE_URL = "https://api.coingecko.com/api/v3"
BASE_DIR = Path(__file__).parent.parent.parent # Projects to the project root 

ENDPOINTS = {
    "bitcoin_list": f"{BASE_URL}/coins/markets?",
    "bitcoin_market_price_data": f"{BASE_URL}/simple/price?"
}

PATHS = {
    'raw': BASE_DIR / 'data' / 'raw',
    'csv_result': BASE_DIR / 'result',
    'processed': BASE_DIR / 'data' / 'processed'
}