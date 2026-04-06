CREATE TABLE crypto_prices (
    id SERIAL PRIMARY KEY,
    coin VARCHAR(50),
    price_usd FLOAT,
    timestamp TIMESTAMP
);

CREATE TABLE crypto_coins (
    id VARCHAR(25),
    name VARCHAR(25),
    symbol VARCHAR(25)
);