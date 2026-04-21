# src/run_analytics.py

import pandas as pd
from sqlalchemy import text
from src.load import get_engine

engine = get_engine()

with engine.connect() as conn:
    result = conn.execute(text(open('sql/latest_prices_query.sql').read()))
    for row in result:
        print(row)