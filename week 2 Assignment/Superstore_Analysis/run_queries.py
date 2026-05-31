import sqlite3
import pandas as pd
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "superstore.db")
output_md = os.path.join(base_dir, "query_results.md")

def df_to_markdown(df):
    headers = list(df.columns)
    markdown_lines = []
    markdown_lines.append("| " + " | ".join(str(h) for h in headers) + " |")
    markdown_lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for _, row in df.iterrows():
        markdown_lines.append("| " + " | ".join(str(val).replace("\n", " ") for val in row) + " |")
    return "\n".join(markdown_lines)

queries = {
    "1.1 Schema Info (Pragma)": "PRAGMA table_info(superstore_sales)",
    "1.2 Total Row Count": "SELECT COUNT(*) AS total_rows FROM superstore_sales",
    "1.3 Sample Data (First 2 rows)": "SELECT row_id, order_id, order_date, customer_name, region, category, sales, profit FROM superstore_sales LIMIT 2",
    
    "2.1 Filter by Region (West, top 5 rows)": "SELECT order_id, customer_name, region, category, sales FROM superstore_sales WHERE region = 'West' LIMIT 5",
    "2.2 Filter by Category (Technology, top 5 rows)": "SELECT order_id, customer_name, category, sub_category, sales FROM superstore_sales WHERE category = 'Technology' LIMIT 5",
    "2.3 Filter by Date (January 2017, top 5 rows)": "SELECT order_id, order_date, customer_name, sales FROM superstore_sales WHERE order_date BETWEEN '2017-01-01' AND '2017-01-31' LIMIT 5",
    "2.4 Filter by Sales (> $1,000, top 5 rows)": "SELECT order_id, customer_name, sales, profit FROM superstore_sales WHERE sales > 1000 LIMIT 5",
    
    "3.1 Category Aggregations": """
        SELECT category, 
               ROUND(SUM(sales), 2) AS total_sales, 
               SUM(quantity) AS total_quantity, 
               ROUND(AVG(sales), 2) AS avg_sales, 
               ROUND(AVG(profit), 2) AS avg_profit 
        FROM superstore_sales 
        GROUP BY category
    """,
    "3.2 Region and Segment Aggregations (Top 8 rows)": """
        SELECT region, segment, 
               ROUND(SUM(sales), 2) AS total_sales, 
               ROUND(AVG(profit), 2) AS avg_profit 
        FROM superstore_sales 
        GROUP BY region, segment
        ORDER BY region, total_sales DESC
        LIMIT 8
    """,
    
    "4.1 Top 5 Products by Sales": """
        SELECT product_name, category, 
               ROUND(SUM(sales), 2) AS total_sales,
               SUM(quantity) AS total_qty
        FROM superstore_sales 
        GROUP BY product_name, category 
        ORDER BY total_sales DESC 
        LIMIT 5
    """,
    "4.2 Top 5 Sub-Categories by Profit": """
        SELECT category, sub_category, 
               ROUND(SUM(profit), 2) AS total_profit 
        FROM superstore_sales 
        GROUP BY category, sub_category 
        ORDER BY total_profit DESC 
        LIMIT 5
    """,
    
    "5.1 Monthly Sales Trends (First 10 months in dataset)": """
        SELECT strftime('%Y-%m', order_date) AS year_month, 
               ROUND(SUM(sales), 2) AS monthly_sales, 
               ROUND(SUM(profit), 2) AS monthly_profit 
        FROM superstore_sales 
        GROUP BY year_month 
        ORDER BY year_month 
        LIMIT 10
    """,
    "5.2 Top 5 Customers by Lifetime Purchase Value": """
        SELECT customer_id, customer_name, segment, 
               ROUND(SUM(sales), 2) AS total_spend,
               COUNT(DISTINCT order_id) AS order_count
        FROM superstore_sales 
        GROUP BY customer_id, customer_name, segment 
        ORDER BY total_spend DESC 
        LIMIT 5
    """,
    "5.3 Duplicate Check (Duplicate Row IDs)": """
        SELECT row_id, COUNT(*) AS occurence_count 
        FROM superstore_sales 
        GROUP BY row_id 
        HAVING COUNT(*) > 1
    """,
    "5.4 Potential Duplicate Transactions (Same Order ID and Product ID)": """
        SELECT order_id, product_id, COUNT(*) AS transaction_count 
        FROM superstore_sales 
        GROUP BY order_id, product_id 
        HAVING COUNT(*) > 1
        LIMIT 5
    """,
    
    "6.1 Null Value Check in Critical Columns": """
        SELECT 
            SUM(CASE WHEN row_id IS NULL THEN 1 ELSE 0 END) AS null_row_ids,
            SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) AS null_order_ids,
            SUM(CASE WHEN order_date IS NULL THEN 1 ELSE 0 END) AS null_order_dates,
            SUM(CASE WHEN customer_name IS NULL THEN 1 ELSE 0 END) AS null_customer_names,
            SUM(CASE WHEN sales IS NULL THEN 1 ELSE 0 END) AS null_sales,
            SUM(CASE WHEN profit IS NULL THEN 1 ELSE 0 END) AS null_profits
        FROM superstore_sales
    """,
    "6.2 Outliers/Invalid Records Check (Non-Positive Sales or Quantity)": """
        SELECT COUNT(*) AS invalid_records 
        FROM superstore_sales 
        WHERE sales <= 0 OR quantity <= 0
    """
}

conn = sqlite3.connect(db_path)

with open(output_md, "w", encoding="utf-8") as f:
    f.write("# Superstore SQL Query Results\n\n")
    f.write("This file contains the output generated by executing SQL queries on the loaded SQLite Superstore database.\n\n")
    
    for title, query in queries.items():
        print(f"Running query: {title}")
        f.write(f"## {title}\n\n")
        f.write("```sql\n" + query.strip() + "\n```\n\n")
        
        try:
            df_res = pd.read_sql_query(query, conn)
            if df_res.empty:
                f.write("*No rows returned.*\n\n")
            else:
                f.write(df_to_markdown(df_res) + "\n\n")
        except Exception as e:
            f.write(f"**Error executing query:** {str(e)}\n\n")
            
        f.write("---\n\n")

conn.close()
print(f"Query execution complete. Results written to {output_md}")
