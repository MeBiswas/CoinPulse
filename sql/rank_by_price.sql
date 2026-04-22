-- Window function rank by price
select
	cc.symbol,
	cc.name,
	cp.coin_id,
	cp.price_usd,
	cp.timestamp,
	ROW_NUMBER() OVER(ORDER BY cp.price_usd DESC) as rank_by_price
from crypto_prices as cp
inner join crypto_coins as cc
	on cp.coin_id = cc.coin_id
order by rank_by_price
;