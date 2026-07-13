-- Advanced Queries (Window Functions, CTEs, Subqueries)

-- 7. Running Totals with Window Functions
-- Calculate running total of revenue per region, ordered by date
WITH daily_revenue AS (
    SELECT 
        o.region_code,
        date(o.order_date) AS order_date,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)) AS daily_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status != 'CANCELLED'
    GROUP BY o.region_code, date(o.order_date)
)
SELECT 
    region_code,
    order_date,
    daily_revenue,
    SUM(daily_revenue) OVER (PARTITION BY region_code ORDER BY order_date) AS running_total
FROM daily_revenue
ORDER BY region_code, order_date;


-- 8. Ranking with DENSE_RANK
-- For each category, rank products by total revenue
WITH product_revenue AS (
    SELECT 
        p.category,
        p.product_name,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)) AS total_revenue
    FROM products p
    JOIN order_items oi ON p.product_id = oi.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.status != 'CANCELLED'
    GROUP BY p.category, p.product_name
)
SELECT 
    category,
    product_name,
    total_revenue,
    DENSE_RANK() OVER (PARTITION BY category ORDER BY total_revenue DESC) AS rank_in_category
FROM product_revenue
ORDER BY category, rank_in_category;


-- 9. LAG/LEAD Analysis
-- Calculate days between consecutive orders for each customer
WITH customer_orders AS (
    SELECT 
        customer_id,
        order_date,
        LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS previous_order_date
    FROM orders
    WHERE customer_id != 'UNKNOWN'
),
gaps AS (
    SELECT 
        customer_id,
        order_date,
        previous_order_date,
        -- SQLite julianday function returns days between two dates
        CASE 
            WHEN previous_order_date IS NOT NULL 
            THEN CAST(julianday(order_date) - julianday(previous_order_date) AS INTEGER)
            ELSE NULL 
        END AS days_gap
    FROM customer_orders
),
customer_avg_gap AS (
    SELECT 
        customer_id,
        AVG(days_gap) AS avg_gap
    FROM gaps
    GROUP BY customer_id
)
SELECT 
    g.customer_id,
    g.order_date,
    g.previous_order_date,
    g.days_gap,
    CASE WHEN a.avg_gap > 30 THEN 'At Risk' ELSE 'Healthy' END AS status_flag
FROM gaps g
JOIN customer_avg_gap a ON g.customer_id = a.customer_id
WHERE g.previous_order_date IS NOT NULL
ORDER BY g.customer_id, g.order_date;


-- 10. CTE with Multiple Levels
-- monthly revenue per customer -> categorize -> count per month
WITH customer_monthly_revenue AS (
    SELECT 
        o.customer_id,
        strftime('%Y-%m', o.order_date) AS order_month,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)) AS monthly_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status != 'CANCELLED' AND o.customer_id != 'UNKNOWN'
    GROUP BY o.customer_id, strftime('%Y-%m', o.order_date)
),
categorized_customers AS (
    SELECT 
        customer_id,
        order_month,
        monthly_revenue,
        CASE 
            WHEN monthly_revenue > 10000 THEN 'High'
            WHEN monthly_revenue >= 5000 THEN 'Medium'
            ELSE 'Low'
        END AS category
    FROM customer_monthly_revenue
)
SELECT 
    order_month,
    category,
    COUNT(customer_id) AS customer_count
FROM categorized_customers
GROUP BY order_month, category
ORDER BY order_month, category;


-- 11. NTILE for Segmentation
-- Divide customers into 4 quartiles based on total lifetime value
WITH customer_ltv AS (
    SELECT 
        c.customer_id,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)) AS total_value
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status != 'CANCELLED'
    GROUP BY c.customer_id
),
quartiles AS (
    SELECT 
        customer_id,
        total_value,
        NTILE(4) OVER (ORDER BY total_value DESC) AS quartile
    FROM customer_ltv
)
SELECT 
    customer_id,
    total_value,
    quartile,
    CASE quartile
        WHEN 1 THEN 'Platinum'
        WHEN 2 THEN 'Gold'
        WHEN 3 THEN 'Silver'
        WHEN 4 THEN 'Bronze'
    END AS quartile_label
FROM quartiles
ORDER BY quartile, total_value DESC;


-- 12. Year-over-Year Comparison
WITH monthly_revenue AS (
    SELECT 
        cast(strftime('%Y', order_date) as integer) AS year,
        cast(strftime('%m', order_date) as integer) AS month,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status != 'CANCELLED'
    GROUP BY strftime('%Y', order_date), strftime('%m', order_date)
),
yoy AS (
    SELECT 
        year,
        month,
        revenue,
        LAG(revenue) OVER (PARTITION BY month ORDER BY year) AS prev_year_revenue
    FROM monthly_revenue
)
SELECT 
    year,
    month,
    revenue,
    prev_year_revenue,
    CASE 
        WHEN prev_year_revenue IS NULL THEN NULL
        ELSE ROUND(((revenue - prev_year_revenue) / prev_year_revenue) * 100, 2)
    END AS yoy_growth_percent
FROM yoy
ORDER BY month, year;


-- 13. First/Last Value Analysis
-- For each customer, show first purchased category and most recent purchased category
WITH customer_purchases AS (
    SELECT 
        o.customer_id,
        o.order_date,
        p.category,
        ROW_NUMBER() OVER (PARTITION BY o.customer_id ORDER BY o.order_date ASC) as rn_asc,
        ROW_NUMBER() OVER (PARTITION BY o.customer_id ORDER BY o.order_date DESC) as rn_desc
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.status != 'CANCELLED' AND o.customer_id != 'UNKNOWN'
),
first_purchase AS (
    SELECT customer_id, category AS first_category FROM customer_purchases WHERE rn_asc = 1
),
last_purchase AS (
    SELECT customer_id, category AS last_category FROM customer_purchases WHERE rn_desc = 1
)
SELECT 
    f.customer_id,
    f.first_category,
    l.last_category,
    CASE WHEN f.first_category != l.last_category THEN 'Yes' ELSE 'No' END AS category_shift
FROM first_purchase f
JOIN last_purchase l ON f.customer_id = l.customer_id;


-- 14. Cumulative Distribution
WITH customer_revenue AS (
    SELECT 
        c.customer_id,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)) AS revenue
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.status != 'CANCELLED'
    GROUP BY c.customer_id
),
total_rev AS (
    SELECT SUM(revenue) as grand_total FROM customer_revenue
),
ranked_customers AS (
    SELECT 
        customer_id,
        revenue,
        SUM(revenue) OVER (ORDER BY revenue DESC) AS cumulative_revenue
    FROM customer_revenue
)
SELECT 
    r.customer_id,
    r.revenue,
    r.cumulative_revenue,
    ROUND((r.cumulative_revenue / t.grand_total) * 100, 2) AS cumulative_percent
FROM ranked_customers r
CROSS JOIN total_rev t
ORDER BY r.revenue DESC;


-- 16. Self-Join with Window Function (Find products frequently bought together)
-- Using a self join on order_items
SELECT 
    oi1.product_id AS product_a,
    oi2.product_id AS product_b,
    COUNT(DISTINCT oi1.order_id) AS times_bought_together
FROM order_items oi1
JOIN order_items oi2 ON oi1.order_id = oi2.order_id 
    AND oi1.product_id < oi2.product_id -- Exclude same product and B-A duplicates
GROUP BY oi1.product_id, oi2.product_id
HAVING times_bought_together > 0
ORDER BY times_bought_together DESC
LIMIT 50;
