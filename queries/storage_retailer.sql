-- VALIDAÇÃO DADOS VENDAS

SELECT 
'retailer_3_prod' as dataset,
store_id as loja,
date(transactions.date) as date,
round(sum(total_value),2) as sum_total_value,
count(distinct(transactions.basket_id)) as distinct_basket_id,

count(1) as n_rows 
FROM `retailer_3_prod.transaction` as transactions 
JOIN `retailer_3_prod.basket` as basket 
ON basket.basket_id = transactions.basket_id 
where date(transactions.date) = DATE_SUB(current_date, INTERVAL 2 day)
group by date, loja

UNION ALL

SELECT 
'muffato_storage' as dataset,
store_id as loja,
dt as date,
round(sum(total_value),2) as sum_total_value,
count(distinct(basket_id)) as distinct_basket_id,

count(1) as n_rows 
FROM `muffato_storage.transactions` 
where dt = DATE_SUB(current_date, INTERVAL 2 day)
group by dt, loja

order by date, loja

-- VALIDAÇÃO DADOS ESTOQUE

SELECT 
'retailer_3_prod' as dataset,
date(date) as date,
store_id as loja,
round(sum(estoque),2) as sum_estoque,
count(distinct(product_id)) as distinct_product_id,
count(1) as n_rows 
FROM `retailer_3_prod.assortment`
where date(date) = DATE_SUB(current_date, INTERVAL 2 day)
group by date, loja
union all
SELECT 
'muffato_storage' as dataset,
dt as date,
store_id as loja,
round(sum(estoque),2) as sum_estoque,
count(distinct(product_id)) as distinct_product_id,
count(1) as n_rows 
FROM `muffato_storage.assortment`  
where dt = DATE_SUB(current_date, INTERVAL 2 day)
group by dt, loja
order by loja


