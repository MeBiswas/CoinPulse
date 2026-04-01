import json
import requests

from datetime import datetime

url = "https://api.coingecko.com/api/v3/simple/price?"



def fetch_data():
    response = requests.get(url, params={
        'ids':'bitcoin',
        'vs_currencies':'usd',
        'x_cg_demo_api_key':'CG-EkZCxz31jraDaKDUUpF8zSrF'
    })
    
    return response.json()

def save_raw_dataset(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/raw/data_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    data = fetch_data()
    save_raw_dataset(data)