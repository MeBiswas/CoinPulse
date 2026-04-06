# utils/config.py

import os

from dotenv import load_dotenv

load_dotenv()

db = os.getenv("DB_NAME")
db_pass = os.getenv("DB_PASSWORD")
db_user = os.getenv("DB_USER_NAME")
api_key = os.getenv("COINGECKO_API_KEY")