SELECT order_id, customer_id, order_date, status, total_amount
FROM   orders
WHERE  status = 'Delivered';

SELECT product_id, product_name, category, brand, unit_price
FROM   products
WHERE  category   = 'Electronics'
  AND  unit_price > 2000;

SELECT customer_id, first_name, last_name, city, state, join_date
FROM   customers
WHERE  state     = 'Maharashtra'
  AND  join_date >= '2024-01-01'
  AND  join_date <  '2025-01-01';

SELECT order_id, customer_id, order_date, status, total_amount
FROM   orders
WHERE  order_date BETWEEN '2024-08-10' AND '2024-08-25'
  AND  status    <> 'Cancelled'
ORDER BY order_date;

-- Q11. idx_orders_date is a B-tree index on orders.order_date. Without it a
-- filter on order_date scans every row; with it the database seeks straight to
-- the matching date range and reads only those rows, which matters a lot at
-- scale. Sample queries that use it:
SELECT order_id, customer_id, status, total_amount
FROM   orders
WHERE  order_date = '2024-08-15';

SELECT order_id, order_date, total_amount
FROM   orders
WHERE  order_date BETWEEN '2024-08-01' AND '2024-08-15';

-- Q12. SELECT * FROM customers WHERE YEAR(join_date) = 2024 does NOT use the
-- index: wrapping join_date in YEAR() means the index (which stores raw dates)
-- can't be matched, forcing a full scan. The SARGable rewrite below compares
-- the raw column to date boundaries, so the index can range-scan it:
SELECT *
FROM   customers
WHERE  join_date >= '2024-01-01'
  AND  join_date <  '2025-01-01';
