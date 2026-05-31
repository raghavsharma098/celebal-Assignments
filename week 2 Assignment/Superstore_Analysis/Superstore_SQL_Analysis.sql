PRAGMA table_info(superstore_sales);

SELECT COUNT(*) AS total_rows
FROM superstore_sales;

SELECT row_id, order_id, order_date, customer_name, region, category, sales, profit
FROM superstore_sales
LIMIT 3;

SELECT order_id, customer_name, region, category, sales
FROM superstore_sales
WHERE region = 'West'
LIMIT 5;

SELECT order_id, customer_name, category, sub_category, sales
FROM superstore_sales
WHERE category = 'Technology'
LIMIT 5;

SELECT order_id, order_date, customer_name, sales
FROM superstore_sales
WHERE order_date BETWEEN '2017-01-01' AND '2017-01-31'
LIMIT 5;

SELECT order_id, customer_name, sales, profit
FROM superstore_sales
WHERE sales > 1000
LIMIT 5;

SELECT category,
       ROUND(SUM(sales), 2) AS total_sales,
       SUM(quantity) AS total_quantity,
       ROUND(AVG(sales), 2) AS avg_sales,
       ROUND(AVG(profit), 2) AS avg_profit
FROM superstore_sales
GROUP BY category;

SELECT region, segment,
       ROUND(SUM(sales), 2) AS total_sales,
       ROUND(AVG(profit), 2) AS avg_profit
FROM superstore_sales
GROUP BY region, segment
ORDER BY region, total_sales DESC;

SELECT product_name, category,
       ROUND(SUM(sales), 2) AS total_sales,
       SUM(quantity) AS total_qty
FROM superstore_sales
GROUP BY product_name, category
ORDER BY total_sales DESC
LIMIT 5;

SELECT category, sub_category,
       ROUND(SUM(profit), 2) AS total_profit
FROM superstore_sales
GROUP BY category, sub_category
ORDER BY total_profit DESC
LIMIT 5;

SELECT strftime('%Y-%m', order_date) AS year_month,
       ROUND(SUM(sales), 2) AS monthly_sales,
       ROUND(SUM(profit), 2) AS monthly_profit
FROM superstore_sales
GROUP BY year_month
ORDER BY year_month
LIMIT 12;

SELECT customer_id, customer_name, segment,
       ROUND(SUM(sales), 2) AS total_spend,
       COUNT(DISTINCT order_id) AS order_count
FROM superstore_sales
GROUP BY customer_id, customer_name, segment
ORDER BY total_spend DESC
LIMIT 5;

SELECT row_id, COUNT(*) AS occurence_count
FROM superstore_sales
GROUP BY row_id
HAVING COUNT(*) > 1;

SELECT order_id, product_id, COUNT(*) AS item_count
FROM superstore_sales
GROUP BY order_id, product_id
HAVING COUNT(*) > 1
LIMIT 10;

SELECT
    SUM(CASE WHEN row_id IS NULL THEN 1 ELSE 0 END) AS null_row_ids,
    SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) AS null_order_ids,
    SUM(CASE WHEN order_date IS NULL THEN 1 ELSE 0 END) AS null_order_dates,
    SUM(CASE WHEN customer_name IS NULL THEN 1 ELSE 0 END) AS null_customer_names,
    SUM(CASE WHEN sales IS NULL THEN 1 ELSE 0 END) AS null_sales,
    SUM(CASE WHEN profit IS NULL THEN 1 ELSE 0 END) AS null_profits
FROM superstore_sales;

SELECT COUNT(*) AS invalid_records
FROM superstore_sales
WHERE sales <= 0 OR quantity <= 0;
