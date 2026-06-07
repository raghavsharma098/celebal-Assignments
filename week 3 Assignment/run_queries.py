import os
import sqlite3
import pandas as pd

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "superstore.db")
output_md = os.path.join(base_dir, "query_results.md")

CT = """
    WITH customer_totals AS (
        SELECT customer_id, SUM(sales) AS total_sales
        FROM orders
        GROUP BY customer_id
    )
"""


def to_markdown(df):
    lines = ["| " + " | ".join(map(str, df.columns)) + " |",
             "| " + " | ".join("---" for _ in df.columns) + " |"]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(v).replace("\n", " ") for v in r) + " |")
    return "\n".join(lines)


queries = [
    ("Step 1 - Table row counts",
     """SELECT 'customers' AS table_name, COUNT(*) AS rows FROM customers
        UNION ALL SELECT 'orders', COUNT(*) FROM orders
        UNION ALL SELECT 'products', COUNT(*) FROM products""", None),

    ("Q1 - Orders with sales above the average (Subquery)",
     """SELECT row_id, order_id, customer_id, ROUND(sales, 2) AS sales
        FROM orders
        WHERE sales > (SELECT AVG(sales) FROM orders)
        ORDER BY sales DESC""", 10),

    ("Q2 - Highest sales order per customer (Subquery)",
     """SELECT o.customer_id, o.order_id, ROUND(o.sales, 2) AS sales
        FROM orders o
        WHERE o.sales = (SELECT MAX(o2.sales) FROM orders o2 WHERE o2.customer_id = o.customer_id)
        ORDER BY o.sales DESC""", 10),

    ("Q3 - Total sales per customer (CTE)",
     CT + """SELECT c.customer_name, ROUND(ct.total_sales, 2) AS total_sales
             FROM customer_totals ct JOIN customers c ON c.customer_id = ct.customer_id
             ORDER BY ct.total_sales DESC""", 10),

    ("Q4 - Customers above average total sales (CTE + Subquery)",
     CT + """SELECT c.customer_name, ROUND(ct.total_sales, 2) AS total_sales
             FROM customer_totals ct JOIN customers c ON c.customer_id = ct.customer_id
             WHERE ct.total_sales > (SELECT AVG(total_sales) FROM customer_totals)
             ORDER BY ct.total_sales DESC""", 10),

    ("Q5 - Rank all customers by total sales (Window Function)",
     CT + """SELECT c.customer_name, ROUND(ct.total_sales, 2) AS total_sales,
                    RANK() OVER (ORDER BY ct.total_sales DESC) AS sales_rank
             FROM customer_totals ct JOIN customers c ON c.customer_id = ct.customer_id
             ORDER BY sales_rank""", 10),

    ("Q6 - Order sequence within each customer (Window + PARTITION BY)",
     """SELECT customer_id, order_id, order_date, ROUND(sales, 2) AS sales,
               ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date, row_id) AS order_seq
        FROM orders
        ORDER BY customer_id, order_seq""", 12),

    ("Q7 - Top 3 customers by total sales (Window Function)",
     CT + """, ranked AS (
                 SELECT c.customer_name, ct.total_sales,
                        RANK() OVER (ORDER BY ct.total_sales DESC) AS sales_rank
                 FROM customer_totals ct JOIN customers c ON c.customer_id = ct.customer_id)
             SELECT customer_name, ROUND(total_sales, 2) AS total_sales, sales_rank
             FROM ranked WHERE sales_rank <= 3 ORDER BY sales_rank""", None),

    ("Step 3 - Final combined: Customer, Total Sales, Rank (JOIN + CTE + Window)",
     CT + """SELECT c.customer_name, ROUND(ct.total_sales, 2) AS total_sales,
                    RANK() OVER (ORDER BY ct.total_sales DESC) AS sales_rank
             FROM customer_totals ct JOIN customers c ON c.customer_id = ct.customer_id
             ORDER BY sales_rank""", 10),

    ("Mini Project Q1 - Top 5 customers",
     CT + """SELECT c.customer_name, ROUND(ct.total_sales, 2) AS total_sales
             FROM customer_totals ct JOIN customers c ON c.customer_id = ct.customer_id
             ORDER BY ct.total_sales DESC LIMIT 5""", None),

    ("Mini Project Q2 - Bottom 5 customers",
     CT + """SELECT c.customer_name, ROUND(ct.total_sales, 2) AS total_sales
             FROM customer_totals ct JOIN customers c ON c.customer_id = ct.customer_id
             ORDER BY ct.total_sales ASC LIMIT 5""", None),

    ("Mini Project Q3 - Customers with only one order",
     """SELECT c.customer_name, COUNT(DISTINCT o.order_id) AS order_count
        FROM orders o JOIN customers c ON c.customer_id = o.customer_id
        GROUP BY o.customer_id, c.customer_name
        HAVING COUNT(DISTINCT o.order_id) = 1
        ORDER BY c.customer_name""", 10),

    ("Mini Project Q4 - Customers with above-average sales",
     CT + """SELECT c.customer_name, ROUND(ct.total_sales, 2) AS total_sales
             FROM customer_totals ct JOIN customers c ON c.customer_id = ct.customer_id
             WHERE ct.total_sales > (SELECT AVG(total_sales) FROM customer_totals)
             ORDER BY ct.total_sales DESC""", 10),

    ("Mini Project Q5 - Highest order value per customer",
     """SELECT c.customer_name, ROUND(MAX(o.sales), 2) AS highest_order_value
        FROM orders o JOIN customers c ON c.customer_id = o.customer_id
        GROUP BY o.customer_id, c.customer_name
        ORDER BY highest_order_value DESC""", 10),
]

conn = sqlite3.connect(db_path)
with open(output_md, "w", encoding="utf-8") as f:
    f.write("# Week 3 - Superstore Query Results\n\n")
    f.write("Output of every query in `analysis.sql`, run against `superstore.db`. ")
    f.write("Large result sets are previewed to a few rows; the full count is noted under each.\n\n")

    for title, sql, limit in queries:
        print("Running:", title)
        df = pd.read_sql_query(sql, conn)
        total = len(df)
        shown = df.head(limit) if limit else df

        f.write(f"## {title}\n\n")
        if limit and total > limit:
            f.write(f"_Showing {limit} of {total} rows._\n\n")
        else:
            f.write(f"_{total} row(s)._\n\n")
        f.write(to_markdown(shown) + "\n\n---\n\n")

conn.close()
print("Done ->", output_md)
