# src/crypto_coins/load_helper.py

import logging
from sqlalchemy import text 

# Gobal
logging.basicConfig(level=logging.INFO)

# ---------------------------
# UPSERT HELPER
# ---------------------------

def upsert_coins(engine, df):
    with engine.begin() as conn:
        
        # 1. TRUNCATE staging table
        conn.execute(text("TRUNCATE TABLE staging_coins;"))

        # 2. Load into staging
        df.to_sql("staging_coins", conn, if_exists="append", index=False, method="multi")

        # 3. Upsert into main table
        conn.execute(text(
            """
            INSERT INTO crypto_coins (symbol, name, coin_id)
            SELECT symbol, name, coin_id
            FROM staging_coins
            ON CONFLICT (coin_id)
            DO UPDATE SET
                symbol = EXCLUDED.symbol,
                name = EXCLUDED.name;
            """
        ))

        logging.info("Coins upsert completed.")