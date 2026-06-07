SELECT 'customers' AS table_name, COUNT(*) AS rows FROM customers
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'products', COUNT(*) FROM products;


SELECT row_id, order_id, customer_id, sales
FROM orders
WHERE sales > (SELECT AVG(sales) FROM orders)
ORDER BY sales DESC;


SELECT o.customer_id, o.order_id, o.sales
FROM orders o
WHERE o.sales = (
        SELECT MAX(o2.sales)
        FROM orders o2
        WHERE o2.customer_id = o.customer_id
      )
ORDER BY o.sales DESC;


WITH customer_totals AS (
    SELECT customer_id, SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT c.customer_id, c.customer_name, ROUND(ct.total_sales, 2) AS total_sales
FROM customer_totals ct
JOIN customers c ON c.customer_id = ct.customer_id
ORDER BY ct.total_sales DESC;


WITH customer_totals AS (
    SELECT customer_id, SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT c.customer_name, ROUND(ct.total_sales, 2) AS total_sales
FROM customer_totals ct
JOIN customers c ON c.customer_id = ct.customer_id
WHERE ct.total_sales > (SELECT AVG(total_sales) FROM customer_totals)
ORDER BY ct.total_sales DESC;


WITH customer_totals AS (
    SELECT customer_id, SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT c.customer_name,
       ROUND(ct.total_sales, 2) AS total_sales,
       RANK() OVER (ORDER BY ct.total_sales DESC) AS sales_rank
FROM customer_totals ct
JOIN customers c ON c.customer_id = ct.customer_id
ORDER BY sales_rank;


SELECT customer_id,
       order_id,
       order_date,
       sales,
       ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, row_id) AS order_seq
FROM orders
ORDER BY customer_id, order_seq;


WITH customer_totals AS (
    SELECT customer_id, SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
),
ranked AS (
    SELECT c.customer_name,
           ct.total_sales,
           RANK() OVER (ORDER BY ct.total_sales DESC) AS sales_rank
    FROM customer_totals ct
    JOIN customers c ON c.customer_id = ct.customer_id
)
SELECT customer_name, ROUND(total_sales, 2) AS total_sales, sales_rank
FROM ranked
WHERE sales_rank <= 3
ORDER BY sales_rank;


WITH customer_totals AS (
    SELECT o.customer_id, SUM(o.sales) AS total_sales
    FROM orders o
    GROUP BY o.customer_id
)
SELECT c.customer_name,
       ROUND(ct.total_sales, 2) AS total_sales,
       RANK() OVER (ORDER BY ct.total_sales DESC) AS sales_rank
FROM customer_totals ct
JOIN customers c ON c.customer_id = ct.customer_id
ORDER BY sales_rank;


WITH customer_totals AS (
    SELECT customer_id, SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT c.customer_name, ROUND(ct.total_sales, 2) AS total_sales
FROM customer_totals ct
JOIN customers c ON c.customer_id = ct.customer_id
ORDER BY ct.total_sales DESC
LIMIT 5;


WITH customer_totals AS (
    SELECT customer_id, SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT c.customer_name, ROUND(ct.total_sales, 2) AS total_sales
FROM customer_totals ct
JOIN customers c ON c.customer_id = ct.customer_id
ORDER BY ct.total_sales ASC
LIMIT 5;


SELECT c.customer_name, COUNT(DISTINCT o.order_id) AS order_count
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
GROUP BY o.customer_id, c.customer_name
HAVING COUNT(DISTINCT o.order_id) = 1
ORDER BY c.customer_name;


WITH customer_totals AS (
    SELECT customer_id, SUM(sales) AS total_sales
    FROM orders
    GROUP BY customer_id
)
SELECT c.customer_name, ROUND(ct.total_sales, 2) AS total_sales
FROM customer_totals ct
JOIN customers c ON c.customer_id = ct.customer_id
WHERE ct.total_sales > (SELECT AVG(total_sales) FROM customer_totals)
ORDER BY ct.total_sales DESC;


SELECT c.customer_name, ROUND(MAX(o.sales), 2) AS highest_order_value
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
GROUP BY o.customer_id, c.customer_name
ORDER BY highest_order_value DESC;
