-- Section D - Joins and Relationships

-- Q19. Each order with the customer's name
SELECT o.order_id,
       o.order_date,
       c.first_name,
       c.last_name,
       o.total_amount
FROM   orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
ORDER BY o.order_date;

-- Q20. All customers and their orders (customers with none show NULLs)
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       o.order_id,
       o.order_date,
       o.status,
       o.total_amount
FROM   customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
ORDER BY c.customer_id, o.order_date;

-- Same idea, used to find customers with no orders at all
SELECT c.customer_id, c.first_name, c.last_name
FROM   customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE  o.order_id IS NULL;

-- Q21. orders -> order_items -> products, with the line total
SELECT o.order_id,
       p.product_name,
       oi.quantity,
       oi.unit_price,
       oi.discount_pct,
       ROUND(oi.unit_price * oi.quantity * (1 - oi.discount_pct / 100), 2) AS line_total
FROM   orders o
JOIN   order_items oi ON o.order_id   = oi.order_id
JOIN   products    p  ON oi.product_id = p.product_id
ORDER BY o.order_id, p.product_name;

-- Q22. LEFT JOIN vs RIGHT JOIN
-- LEFT JOIN keeps every row from the left table; here it shows all customers
-- even if they never ordered. RIGHT JOIN keeps every row from the right table,
-- so it would show all orders even if the customer record was missing.
-- A FULL OUTER JOIN keeps unmatched rows from both sides at once, which is handy
-- for reconciliation - finding customers with no orders and orphaned orders in
-- one query. MySQL has no FULL OUTER JOIN, so it is emulated with UNION:
SELECT c.customer_id, c.first_name, o.order_id
FROM   customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
UNION
SELECT c.customer_id, c.first_name, o.order_id
FROM   customers c
RIGHT JOIN orders o ON c.customer_id = o.customer_id
WHERE  c.customer_id IS NULL;

-- Q23. Foreign keys
-- orders.customer_id -> customers.customer_id
-- order_items.order_id -> orders.order_id
-- order_items.product_id -> products.product_id
-- Inserting an order with customer_id = 999 fails with a foreign-key error,
-- because no such customer exists. The constraint keeps every order tied to a
-- real customer (no orphaned rows).
-- INSERT INTO orders VALUES (1099, 999, '2024-09-01', 'Pending', 500.00);
