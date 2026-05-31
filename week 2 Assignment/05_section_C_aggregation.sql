-- Section C - Aggregation

-- Q13. Total number of orders
SELECT COUNT(*) AS total_orders
FROM   orders;

-- Q14. Total revenue from delivered orders
SELECT SUM(total_amount) AS total_revenue_delivered
FROM   orders
WHERE  status = 'Delivered';

-- Q15. Average unit price per category
SELECT   category,
         ROUND(AVG(unit_price), 2) AS avg_unit_price
FROM     products
GROUP BY category
ORDER BY avg_unit_price DESC;

-- Q16. Order count and revenue per status, highest revenue first
SELECT   status,
         COUNT(*)          AS order_count,
         SUM(total_amount) AS total_revenue
FROM     orders
GROUP BY status
ORDER BY total_revenue DESC;

-- Q17. Most expensive and cheapest product price per category
SELECT   category,
         MAX(unit_price) AS most_expensive,
         MIN(unit_price) AS cheapest
FROM     products
GROUP BY category
ORDER BY category;

-- Q18. Categories whose average unit price is over 2000
-- HAVING filters after the grouping, which is why WHERE can't be used here.
SELECT   category,
         ROUND(AVG(unit_price), 2) AS avg_price
FROM     products
GROUP BY category
HAVING   AVG(unit_price) > 2000
ORDER BY avg_price DESC;
