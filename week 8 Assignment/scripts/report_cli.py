import sqlite3
import argparse
from datetime import datetime
import os
try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False

DB_PATH = 'ecommerce.db'

def get_connection():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database {DB_PATH} not found. Please run load_data.py first.")
        exit(1)
    return sqlite3.connect(DB_PATH)

def format_table(data, headers):
    if not data:
        return "No data found."
    if HAS_TABULATE:
        return tabulate(data, headers=headers, tablefmt="grid")
    else:
        # Fallback simple formatter
        col_widths = [max(len(str(item)) for item in col) for col in zip(*data, headers)]
        format_str = " | ".join(f"{{:<{width}}}" for width in col_widths)
        header_str = format_str.format(*headers)
        separator = "-" * len(header_str)
        rows_str = "\n".join(format_str.format(*row) for row in data)
        return f"{header_str}\n{separator}\n{rows_str}"

def generate_summary(start_date, end_date, period_type='monthly'):
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Total orders, revenue, unique customers in current period
    query_current = """
        SELECT 
            COUNT(DISTINCT o.order_id) as total_orders,
            SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)) as total_revenue,
            COUNT(DISTINCT o.customer_id) as unique_customers
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_date >= ? AND o.order_date <= ? AND o.status != 'CANCELLED'
    """
    cursor.execute(query_current, (start_date, end_date))
    current_stats = cursor.fetchone()
    
    total_orders = current_stats[0] or 0
    total_revenue = current_stats[1] or 0.0
    unique_customers = current_stats[2] or 0
    
    # Determine previous period
    # simple approximation for previous period based on days
    dt_start = datetime.strptime(start_date, '%Y-%m-%d')
    dt_end = datetime.strptime(end_date, '%Y-%m-%d')
    days_diff = (dt_end - dt_start).days
    
    # SQLite datetime modifiers: '-N days'
    query_prev = """
        SELECT 
            SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)) as total_revenue
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_date >= date(?, '-' || ? || ' days') 
          AND o.order_date < ? 
          AND o.status != 'CANCELLED'
    """
    cursor.execute(query_prev, (start_date, str(days_diff + 1), start_date))
    prev_stats = cursor.fetchone()
    prev_revenue = prev_stats[0] or 0.0
    
    revenue_growth = 0.0
    if prev_revenue > 0:
        revenue_growth = ((total_revenue - prev_revenue) / prev_revenue) * 100
    
    # 2. Top 3 products
    query_top_products = """
        SELECT 
            p.product_name,
            SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)) as revenue
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN products p ON oi.product_id = p.product_id
        WHERE o.order_date >= ? AND o.order_date <= ? AND o.status != 'CANCELLED'
        GROUP BY p.product_id, p.product_name
        ORDER BY revenue DESC
        LIMIT 3
    """
    cursor.execute(query_top_products, (start_date, end_date))
    top_products = cursor.fetchall()
    
    print("\n" + "="*50)
    print(f" SUMMARY REPORT ({start_date} to {end_date})")
    print("="*50)
    
    summary_data = [
        ["Total Orders", total_orders],
        ["Total Revenue ($)", f"{total_revenue:.2f}"],
        ["Unique Customers", unique_customers],
        ["Prev Period Revenue ($)", f"{prev_revenue:.2f}"],
        ["Revenue Growth (%)", f"{revenue_growth:.2f}%"]
    ]
    print(format_table(summary_data, ["Metric", "Value"]))
    
    print("\n--- TOP 3 PRODUCTS ---")
    if top_products:
        print(format_table(top_products, ["Product Name", "Revenue ($)"]))
    else:
        print("No products sold in this period.")
        
    conn.close()

def run_specific_report(report_name):
    conn = get_connection()
    cursor = conn.cursor()
    
    if report_name == 'revenue':
        print("\n--- Total Revenue per Category ---")
        with open('sql/aggregations.sql', 'r') as f:
            sql = f.read()
        # Find the specific query (query 1)
        # For simplicity, we just execute the known SQL here:
        query = """
            SELECT p.category, SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)) AS total_revenue
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            JOIN orders o ON oi.order_id = o.order_id
            WHERE o.status != 'CANCELLED'
            GROUP BY p.category ORDER BY total_revenue DESC;
        """
        cursor.execute(query)
        print(format_table(cursor.fetchall(), ["Category", "Total Revenue"]))
        
    elif report_name == 'top_customers':
        print("\n--- Top 10 Customers by Revenue ---")
        query = """
            SELECT c.customer_name, SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent/100.0)) AS total_revenue
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            JOIN order_items oi ON o.order_id = oi.order_id
            WHERE o.status != 'CANCELLED'
            GROUP BY c.customer_id, c.customer_name ORDER BY total_revenue DESC LIMIT 10;
        """
        cursor.execute(query)
        print(format_table(cursor.fetchall(), ["Customer Name", "Total Revenue"]))
        
    elif report_name == 'retention':
        print("\n--- Cohort Retention Analysis ---")
        with open('sql/cohort_analysis.sql', 'r') as f:
            query = f.read()
        cursor.execute(query)
        columns = [description[0] for description in cursor.description]
        print(format_table(cursor.fetchall(), columns))
    else:
        print(f"Unknown report type: {report_name}")
        
    conn.close()

def main():
    parser = argparse.ArgumentParser(description="E-Commerce Analytics Reporting CLI")
    parser.add_argument('--start-date', type=str, help="Start date (YYYY-MM-DD)")
    parser.add_argument('--end-date', type=str, help="End date (YYYY-MM-DD)")
    parser.add_argument('--period', type=str, choices=['daily', 'weekly', 'monthly'], default='monthly', help="Reporting period type")
    parser.add_argument('--report', type=str, choices=['revenue', 'top_customers', 'retention'], help="Run a specific pre-defined report")
    
    args = parser.parse_args()
    
    if args.report:
        run_specific_report(args.report)
    elif args.start_date and args.end_date:
        generate_summary(args.start_date, args.end_date, args.period)
    else:
        print("Please provide either --report or both --start-date and --end-date.")
        parser.print_help()

if __name__ == "__main__":
    main()
