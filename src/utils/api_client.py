# utils/api_client.py

import logging
import requests

from requests.exceptions import HTTPError

def fetch_data(url, params=None, headers=None):
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        logging.info('Request Successfully!')
        return response.json()

    except HTTPError as http_err:
        logging.error(f"HTTP Error: {http_err}")
        return None
    
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return None