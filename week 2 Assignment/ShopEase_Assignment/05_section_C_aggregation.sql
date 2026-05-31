SELECT COUNT(*) AS total_orders
FROM   orders;

SELECT SUM(total_amount) AS total_revenue_delivered
FROM   orders
WHERE  status = 'Delivered';

SELECT   category,
         ROUND(AVG(unit_price), 2) AS avg_unit_price
FROM     products
GROUP BY category
ORDER BY avg_unit_price DESC;

SELECT   status,
         COUNT(*)          AS order_count,
         SUM(total_amount) AS total_revenue
FROM     orders
GROUP BY status
ORDER BY total_revenue DESC;

SELECT   category,
         MAX(unit_price) AS most_expensive,
         MIN(unit_price) AS cheapest
FROM     products
GROUP BY category
ORDER BY category;

SELECT p.category,
       p.product_name     AS most_expensive_product,
       p.unit_price       AS max_price,
       cheap.product_name AS cheapest_product,
       cheap.unit_price   AS min_price
FROM   products p
JOIN (
    SELECT category, MAX(unit_price) AS max_price
    FROM   products
    GROUP BY category
) mx ON p.category = mx.category AND p.unit_price = mx.max_price
JOIN (
    SELECT p2.category, p2.product_name, p2.unit_price,
           ROW_NUMBER() OVER (PARTITION BY p2.category ORDER BY p2.unit_price ASC) AS rn
    FROM   products p2
) cheap ON cheap.category = p.category AND cheap.rn = 1
ORDER BY p.category;

SELECT   category,
         ROUND(AVG(unit_price), 2) AS avg_price
FROM     products
GROUP BY category
HAVING   AVG(unit_price) > 2000
ORDER BY avg_price DESC;
