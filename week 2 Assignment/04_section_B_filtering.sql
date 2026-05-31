-- Section B - Filtering and Optimization

-- Q7. All delivered orders
SELECT order_id, customer_id, order_date, status, total_amount
FROM   orders
WHERE  status = 'Delivered';

-- Q8. Electronics priced over 2000
SELECT product_id, product_name, category, brand, unit_price
FROM   products
WHERE  category = 'Electronics'
  AND  unit_price > 2000;

-- Q9. Customers from Maharashtra who joined in 2024
-- Using a date range instead of YEAR() so the join_date index can be used.
SELECT customer_id, first_name, last_name, city, state, join_date
FROM   customers
WHERE  state = 'Maharashtra'
  AND  join_date >= '2024-01-01'
  AND  join_date <  '2025-01-01';

-- Q10. Orders from 2024-08-10 to 2024-08-25 (inclusive) that are not cancelled
SELECT order_id, customer_id, order_date, status, total_amount
FROM   orders
WHERE  order_date BETWEEN '2024-08-10' AND '2024-08-25'
  AND  status <> 'Cancelled'
ORDER BY order_date;

-- Q11. What idx_orders_date does
-- It is a B-tree index on orders.order_date. A query that filters by date can
-- seek straight to the matching range instead of scanning the whole table,
-- which matters a lot once the table is large.
-- Example queries that benefit:
SELECT order_id, customer_id, status, total_amount
FROM   orders
WHERE  order_date = '2024-08-15';

SELECT order_id, order_date, total_amount
FROM   orders
WHERE  order_date BETWEEN '2024-08-01' AND '2024-08-15';

-- Q12. Would the index be used for YEAR(join_date) = 2024?
-- No. Wrapping the column in YEAR() means the index (which stores raw dates)
-- can't be used, so it falls back to a full scan. Rewrite it as a range so the
-- index works:
SELECT *
FROM   customers
WHERE  join_date >= '2024-01-01'
  AND  join_date <  '2025-01-01';
