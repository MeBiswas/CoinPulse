-- Daily Averages
select
	cc.symbol,
	cc.name,
    DATE(cp.timestamp) as date,
	AVG(cp.price_usd) as daily_avg
from crypto_prices as cp
inner join crypto_coins as cc
	on cp.coin_id = cc.coin_id
group by cc.symbol, cc.name, DATE(cp.timestamp)
order by cc.name, DATE(cp.timestamp) desc
;

-- Latest Day's Average
-- select
--     cc.symbol,
--     cc.name,
--     DATE(cp.timestamp) as date,
--     AVG(cp.price_usd) as daily_avg
-- from crypto_prices cp
-- inner join crypto_coins cc
--     on cp.coin_id = cc.coin_id
-- where DATE(cp.timestamp) = (select MAX(DATE(timestamp)) from crypto_prices)
-- group by cc.symbol, cc.name
-- order by cc.name
-- ;