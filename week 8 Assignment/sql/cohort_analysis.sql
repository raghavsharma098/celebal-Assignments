-- 15. Complex CTE: Cohort Analysis
-- Group customers by registration month (cohort)
-- Calculate how many ordered in month 0, month 1, month 2, month 3
-- Retention rate for each month

WITH customer_cohorts AS (
    SELECT 
        customer_id,
        strftime('%Y-%m', registration_date) AS cohort_month
    FROM customers
    WHERE customer_id != 'UNKNOWN'
),
customer_orders AS (
    SELECT 
        o.customer_id,
        strftime('%Y-%m', o.order_date) AS order_month
    FROM orders o
    WHERE o.status != 'CANCELLED' AND o.customer_id != 'UNKNOWN'
    GROUP BY o.customer_id, strftime('%Y-%m', o.order_date)
),
cohort_activities AS (
    SELECT 
        cc.customer_id,
        cc.cohort_month,
        co.order_month,
        -- Calculate the difference in months between cohort_month and order_month
        -- SQLite doesn't have a direct DATEDIFF for months, so we compute it using year and month
        (CAST(strftime('%Y', co.order_month || '-01') AS INTEGER) - CAST(strftime('%Y', cc.cohort_month || '-01') AS INTEGER)) * 12 + 
        (CAST(strftime('%m', co.order_month || '-01') AS INTEGER) - CAST(strftime('%m', cc.cohort_month || '-01') AS INTEGER)) AS month_diff
    FROM customer_cohorts cc
    LEFT JOIN customer_orders co ON cc.customer_id = co.customer_id
),
cohort_sizes AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT customer_id) AS total_customers
    FROM customer_cohorts
    GROUP BY cohort_month
),
retention_counts AS (
    SELECT 
        cohort_month,
        month_diff,
        COUNT(DISTINCT customer_id) AS customers_retained
    FROM cohort_activities
    WHERE month_diff >= 0 AND month_diff <= 3
    GROUP BY cohort_month, month_diff
)
SELECT 
    r.cohort_month,
    s.total_customers AS cohort_size,
    SUM(CASE WHEN r.month_diff = 0 THEN r.customers_retained ELSE 0 END) AS month_0_retained,
    SUM(CASE WHEN r.month_diff = 1 THEN r.customers_retained ELSE 0 END) AS month_1_retained,
    SUM(CASE WHEN r.month_diff = 2 THEN r.customers_retained ELSE 0 END) AS month_2_retained,
    SUM(CASE WHEN r.month_diff = 3 THEN r.customers_retained ELSE 0 END) AS month_3_retained,
    
    ROUND(SUM(CASE WHEN r.month_diff = 0 THEN r.customers_retained ELSE 0 END) * 100.0 / s.total_customers, 2) AS month_0_retention_rate,
    ROUND(SUM(CASE WHEN r.month_diff = 1 THEN r.customers_retained ELSE 0 END) * 100.0 / s.total_customers, 2) AS month_1_retention_rate,
    ROUND(SUM(CASE WHEN r.month_diff = 2 THEN r.customers_retained ELSE 0 END) * 100.0 / s.total_customers, 2) AS month_2_retention_rate,
    ROUND(SUM(CASE WHEN r.month_diff = 3 THEN r.customers_retained ELSE 0 END) * 100.0 / s.total_customers, 2) AS month_3_retention_rate
FROM retention_counts r
JOIN cohort_sizes s ON r.cohort_month = s.cohort_month
GROUP BY r.cohort_month, s.total_customers
ORDER BY r.cohort_month;
