-- Dimension Table
CREATE TABLE crypto_coins (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(25) NOT NULL,
    name VARCHAR(25) NOT NULL UNIQUE,
    coin_id VARCHAR(50) NOT NULL UNIQUE
);

-- Fact Table
CREATE TABLE crypto_prices (
    id SERIAL PRIMARY KEY,
    price_usd FLOAT NOT NULL,
    coin_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL

    CONSTRAINT fk_coin
        FOREIGN KEY (coin_id),
        REFERENCES crypto_coins(coin_id)
);

-- 3. Add Indexes (Optimization layer)
CREATE INDEX idx_coin_id ON crypto_prices(coin_id);
CREATE INDEX idx_timestamp ON crypto_prices(timestamp);
