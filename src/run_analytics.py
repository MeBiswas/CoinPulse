# src/run_analytics.py

import logging
import pandas as pd
from sqlalchemy import text
from tabulate import tabulate
from src.load import get_engine

from src.utils import PATHS

# Gobal
logging.basicConfig(level=logging.INFO)

QUERIES = {
    'top_movers': 'sql/top_movers.sql',
    'daily_avg': 'sql/daily_average.sql',
    'rank_by_price': 'sql/rank_by_price.sql',
    'latest_prices': 'sql/latest_prices_query.sql'
}

def run_query(name, filepath, export):
    try:
        engine = get_engine()
        
        sql_query = text(open(filepath).read())
        df = pd.read_sql(sql_query, engine)
        print(f'\n--- {name} ---')
        print(tabulate(df, headers='keys', tablefmt='grid'))
        
        if export:
            output_dir = PATHS['csv_result']
            output_dir.mkdir(parents=True, exist_ok=True)
            df.to_csv(output_dir / f'{name}.csv', index=False)
    except Exception as e:
        logging.error(f"Error in query '{name}': {e}")

def run_all_queries(export):
    for name, filepath in QUERIES.items():
        run_query(name, filepath, export)
        
if __name__ == '__main__':
    run_all_queries(export=True)