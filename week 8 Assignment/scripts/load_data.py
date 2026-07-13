import sqlite3
import pandas as pd
import os

def load_data():
    db_path = 'ecommerce.db'
    
    # Remove existing db to start fresh
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Create Schema
    with open('sql/schema.sql', 'r') as f:
        schema_sql = f.read()
    
    cursor.executescript(schema_sql)
    print("Schema created.")
    
    # 2. Load Cleaned CSVs
    try:
        df_customers = pd.read_csv('data/cleaned/customers_clean.csv')
        df_products = pd.read_csv('data/cleaned/products_clean.csv')
        df_orders = pd.read_csv('data/cleaned/orders_clean.csv', keep_default_na=False, na_values=[''])
        df_order_items = pd.read_csv('data/cleaned/order_items_clean.csv')
    except FileNotFoundError:
        print("Cleaned CSV files not found. Please run clean_data.py first.")
        return
        
    df_customers.to_sql('customers', conn, if_exists='append', index=False)
    df_products.to_sql('products', conn, if_exists='append', index=False)
    df_orders.to_sql('orders', conn, if_exists='append', index=False)
    df_order_items.to_sql('order_items', conn, if_exists='append', index=False)
    
    print("Cleaned data successfully loaded into SQLite database.")
    
    # Verify row counts
    print("\n--- Row Counts ---")
    tables = ['customers', 'products', 'orders', 'order_items']
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table}: {count} rows")
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    load_data()
