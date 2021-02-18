-- VALIDAÇÃO DADOS VENDAS

SELECT 'retailer_3_prod' as dataset, date(transactions.date) as date ,sum(total_value) as sum_total_value, count(distinct(transactions.basket_id)) as distinct_basket_id, count(distinct(store_id)) as distinct_store_id,count(store_id) as n_store_id, count(1) as n_rows FROM `retailer_3_prod.transaction` as transactions JOIN `retailer_3_prod.basket` as basket ON basket.basket_id = transactions.basket_id where date(transactions.date) between '2020-12-01' and '2021-01-31' and store_id in ("3_74","3_75","3_76") group by date
union all
SELECT 'muffato_storage' as dataset, dt as date,sum(total_value) as sum_total_value, count(distinct(basket_id)) as distinct_basket_id, count(distinct(store_id)) as distinct_store_id,count(store_id) as n_store_id, count(1) as n_rows FROM `muffato_storage.transactions` where dt between '2020-12-01' and '2021-01-31' and store_id in ("3_74","3_75","3_76") group by dt
order by date

-- VALIDAÇÃO DADOS ESTOQUE

SELECT 'retailer_3_prod' as dataset, date(date), sum(estoque) as sum_estoque, count(distinct(product_id)) as distinct_product_id, count(distinct(store_id)) as distinct_store_id,count(store_id) as n_store_id, count(1) as n_rows FROM `retailer_3_prod.assortment` where date(date) between '2020-07-01' and '2020-10-31' group by date
union all
SELECT 'muffato_storage' as dataset, dt, sum(estoque) as sum_estoque, count(distinct(product_id)) as distinct_product_id, count(distinct(store_id)) as distinct_store_id,count(store_id) as n_store_id, count(1) as n_rows FROM `muffato_storage.assortment`  where dt between '2020-07-01' and '2020-10-31' group by dt
order by dataset, date

-- VALIDAÇÃO POR LOJAS

(SELECT
"storage" as DB,
EXTRACT(MONTH FROM dt) as month,
s_id as store_id,
count(distinct dt) as n_days
FROM muffato_storage.transactions 
WHERE s_id in ("3_74","3_75","3_76") and dt between "2020-12-01" and "2021-01-31" 
GROUP BY s_id, month)

UNION ALL

(SELECT
"retailer_3" as DB,
EXTRACT(MONTH FROM sales.date) as month,
store_id as store_id,
count(distinct DATE(sales.date)) as n_days
FROM retailer_3_prod.transaction as sales
JOIN retailer_3_prod.basket as basket
USING (basket_id)
WHERE store_id in ("3_74","3_75","3_76") and DATE(sales.date) between "2020-12-01" and "2021-01-31" 
GROUP BY store_id, month)

ORDER BY month, store_id
