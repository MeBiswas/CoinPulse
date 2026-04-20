DROP TABLE IF EXISTS crypto_prices;
DROP TABLE IF EXISTS crypto_coins;

-- Dimension Table
CREATE TABLE IF NOT EXISTS crypto_coins (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(25) NOT NULL,
    name VARCHAR(100) NOT NULL UNIQUE,
    coin_id VARCHAR(100) NOT NULL UNIQUE
);

ALTER TABLE crypto_coins
DROP CONSTRAINT IF EXISTS crypto_coins_name_key;

-- Fact Table
CREATE TABLE IF NOT EXISTS crypto_prices (
    timestamp TIMESTAMP NOT NULL,
    coin_id VARCHAR(100) NOT NULL,
    price_usd NUMERIC(18,8) NOT NULL,
    PRIMARY KEY (coin_id, timestamp),

    CONSTRAINT fk_coin
        FOREIGN KEY (coin_id)
        REFERENCES crypto_coins(coin_id)
);

-- Index for time-based queries
CREATE INDEX IF NOT EXISTS idx_timestamp
ON crypto_prices(timestamp);
