-- 1. Latest Prices Query
-- Retrieves the most recent price for each cryptocurrency
select
	cc.name,
	cc.symbol,
	cp.price_usd,
	cp.timestamp
from crypto_prices as cp
inner join crypto_coins as cc
	on cp.coin_id = cc.coin_id
where cp.timestamp = (
	select max(timestamp)
	from crypto_prices
)
order by cc.name asc
;

-- Alternative: Using ROW_NUMBER() window function
select 
	cc.symbol,
	cc.name,
	cp.price_usd,
	cp.timestamp
from (select 
		coin_id,
		price_usd,
		timestamp,
		ROW_NUMBER() OVER(PARTITION BY coin_id ORDER BY timestamp DESC) as rn
	from crypto_prices) as cp
inner join crypto_coins as cc
 on cp.coin_id = cc.coin_id
where cp.rn = 1
order by name
;
