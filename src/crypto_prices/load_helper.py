# src/crypto_prices/load_helper.py

import logging
import pandas as pd
from sqlalchemy import text

# ---------------------------
# UPSERT HELPER
# ---------------------------

def upsert_prices(engine, df):
    with engine.begin() as conn:
        
        # 1. TRUNCATE staging table
        conn.execute(text("TRUNCATE TABLE staging_prices;"))
        
        # 2. Load into staging
        df.to_sql("staging_prices", conn, if_exists="append", index=False, method="multi")

        # 3. Upsert into fact table
        conn.execute(text(
            """
            INSERT INTO crypto_prices (coin_id, timestamp, price_usd)
            SELECT coin_id, timestamp::timestamp, price_usd
            FROM staging_prices
            ON CONFLICT (coin_id, timestamp)
            DO UPDATE SET
                price_usd = EXCLUDED.price_usd;
            """
        ))

        logging.info("Prices upsert completed.")