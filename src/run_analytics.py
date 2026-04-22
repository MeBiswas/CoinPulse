# src/run_analytics.py

import pandas as pd
from sqlalchemy import text
from src.load import get_engine

QUERIES = {
    'top_movers': 'sql/top_movers.sql',
    'daily_avg': 'sql/daily_average.sql',
    'rank_by_price': 'sql/rank_by_price.sql',
    'latest_prices': 'sql/latest_prices_query.sql'
}

def run_query(name, filepath):
    engine = get_engine()
    
    with engine.connect() as conn:
        result = conn.execute(text(open(filepath).read()))
        print(f'\n--- {name} ---')
        for row in result:
            print(row)

def run_all_queries():
    for name, filepath in QUERIES.items():
        run_query(name, filepath)
        
if __name__ == '__main__':
    run_all_queries()