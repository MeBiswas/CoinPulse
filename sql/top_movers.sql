-- Top Gainers and Losers (comparing latest price to previous price)
WITH price_changes AS (
    SELECT
        cc.symbol,
        cc.name,
        LAG(cp.price_usd) OVER (PARTITION BY cp.coin_id ORDER BY cp.timestamp) as previous_price,
        cp.price_usd as current_price,
        cp.timestamp,
        ROW_NUMBER() OVER (PARTITION BY cp.coin_id ORDER BY cp.timestamp DESC) as rn
    FROM crypto_prices cp
    INNER JOIN crypto_coins cc ON cp.coin_id = cc.coin_id
)
SELECT
    symbol,
    name,
    current_price,
    previous_price,
    ROUND((current_price - previous_price)::numeric, 2) as price_change,
    ROUND(((current_price - previous_price) / previous_price * 100)::numeric, 2) as percent_change
FROM price_changes
WHERE rn = 1 AND previous_price IS NOT NULL
ORDER BY percent_change DESC
LIMIT 10;