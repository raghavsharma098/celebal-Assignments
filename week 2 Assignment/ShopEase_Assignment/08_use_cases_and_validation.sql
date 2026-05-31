SELECT   DATE_FORMAT(order_date, '%Y-%m') AS year_month,
         COUNT(*)          AS total_orders,
         SUM(total_amount) AS monthly_revenue,
         ROUND(AVG(total_amount), 2) AS avg_order_value
FROM     orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY year_month;

SELECT   DATE_FORMAT(o.order_date, '%Y-%m') AS year_month,
         p.category,
         COUNT(DISTINCT o.order_id)          AS orders_with_category,
         SUM(oi.quantity)                    AS units_sold,
         ROUND(SUM(oi.unit_price * oi.quantity * (1 - oi.discount_pct / 100)), 2) AS category_revenue
FROM     orders      o
JOIN     order_items oi ON o.order_id    = oi.order_id
JOIN     products    p  ON oi.product_id = p.product_id
GROUP BY DATE_FORMAT(o.order_date, '%Y-%m'), p.category
ORDER BY year_month, category_revenue DESC;

SELECT   c.customer_id,
         CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
         c.city,
         c.is_premium,
         COUNT(o.order_id)    AS total_orders,
         SUM(o.total_amount)  AS lifetime_value,
         ROUND(AVG(o.total_amount), 2) AS avg_order_value
FROM     customers c
JOIN     orders    o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.city, c.is_premium
ORDER BY lifetime_value DESC
LIMIT 5;

SELECT   c.customer_id,
         CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
         COUNT(o.order_id)    AS delivered_orders,
         SUM(o.total_amount)  AS confirmed_revenue
FROM     customers c
JOIN     orders    o ON c.customer_id = o.customer_id
WHERE    o.status = 'Delivered'
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY confirmed_revenue DESC;

SELECT   p.product_id,
         p.product_name,
         p.category,
         SUM(oi.quantity)            AS total_qty_sold,
         COUNT(DISTINCT oi.order_id) AS appeared_in_orders
FROM     products    p
JOIN     order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_qty_sold DESC
LIMIT 3;

SELECT   email, COUNT(*) AS email_count
FROM     customers
GROUP BY email
HAVING   COUNT(*) > 1;

SELECT   order_id, product_id, COUNT(*) AS duplicate_count
FROM     order_items
GROUP BY order_id, product_id
HAVING   COUNT(*) > 1;

SELECT   customer_id, order_date, COUNT(*) AS order_count
FROM     orders
GROUP BY customer_id, order_date
HAVING   COUNT(*) > 1;

SELECT 'customers'   AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL
SELECT 'products',    COUNT(*) FROM products
UNION ALL
SELECT 'orders',      COUNT(*) FROM orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items;

SELECT 'customers - null email'         AS check_name, COUNT(*) AS null_count FROM customers   WHERE email IS NULL
UNION ALL
SELECT 'orders - null customer_id',     COUNT(*) FROM orders      WHERE customer_id IS NULL
UNION ALL
SELECT 'order_items - null product_id', COUNT(*) FROM order_items WHERE product_id IS NULL
UNION ALL
SELECT 'products - null unit_price',    COUNT(*) FROM products    WHERE unit_price IS NULL;

SELECT   o.order_id,
         o.total_amount AS order_total,
         ROUND(SUM(oi.unit_price * oi.quantity * (1 - oi.discount_pct / 100)), 2) AS calculated_total,
         ROUND(o.total_amount - SUM(oi.unit_price * oi.quantity * (1 - oi.discount_pct / 100)), 2) AS discrepancy
FROM     orders      o
JOIN     order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id, o.total_amount
ORDER BY o.order_id;

SELECT product_id, product_name, category, stock_qty
FROM   products
WHERE  stock_qty < 150
ORDER BY stock_qty ASC;

SELECT o.order_id, o.customer_id, o.order_date, o.status
FROM   orders o
LEFT JOIN order_items oi ON o.order_id = oi.order_id
WHERE  oi.item_id IS NULL;
