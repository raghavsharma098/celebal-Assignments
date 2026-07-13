-- Basic Queries

-- 1. Total revenue per category
-- revenue = quantity * unit_price * (1 - discount_percent/100)
SELECT 
    p.category,
    SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)) AS total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.status != 'CANCELLED'
GROUP BY p.category
ORDER BY total_revenue DESC;


-- 2. Top 10 customers by total order value
SELECT 
    c.customer_id,
    c.customer_name,
    SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)) AS total_order_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status != 'CANCELLED'
GROUP BY c.customer_id, c.customer_name
ORDER BY total_order_value DESC
LIMIT 10;


-- 3. Month-wise order count for the last 12 months
SELECT 
    strftime('%Y-%m', order_date) AS order_month,
    COUNT(DISTINCT order_id) AS order_count
FROM orders
-- Assuming current date is max order_date, or we just take the last 12 months available in data
WHERE order_date >= date((SELECT MAX(order_date) FROM orders), '-12 months')
GROUP BY order_month
ORDER BY order_month;


-- Intermediate Queries

-- 4. Find customers who placed orders but never had any item delivered
SELECT 
    c.customer_id,
    c.customer_name
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING SUM(CASE WHEN o.status = 'DELIVERED' THEN 1 ELSE 0 END) = 0
   AND COUNT(o.order_id) > 0;


-- 5. Products that were ordered but had more returns than purchases
-- quantity < 0 means return
SELECT 
    p.product_id,
    p.product_name,
    SUM(CASE WHEN oi.quantity > 0 THEN oi.quantity ELSE 0 END) AS total_purchased,
    SUM(CASE WHEN oi.quantity < 0 THEN ABS(oi.quantity) ELSE 0 END) AS total_returned
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name
HAVING total_returned > total_purchased;


-- 6. Calculate the return rate (returned items / total items) per category
SELECT 
    p.category,
    SUM(CASE WHEN oi.quantity < 0 THEN ABS(oi.quantity) ELSE 0 END) AS total_returned_items,
    SUM(ABS(oi.quantity)) AS total_items,
    CAST(SUM(CASE WHEN oi.quantity < 0 THEN ABS(oi.quantity) ELSE 0 END) AS FLOAT) / SUM(ABS(oi.quantity)) AS return_rate
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.category;
