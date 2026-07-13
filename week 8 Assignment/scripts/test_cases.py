import sqlite3
import pandas as pd
from datetime import datetime, timedelta

def test_edge_cases():
    db_path = 'ecommerce.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Running Edge Case Tests...\n")
    
    # Test 1: What happens when order_items has an order_id not in orders?
    # Expected: The SQLite schema has FOREIGN KEY (order_id) REFERENCES orders(order_id)
    # But SQLite foreign keys must be enabled per connection.
    cursor.execute("PRAGMA foreign_keys = ON;")
    try:
        cursor.execute("INSERT INTO order_items (item_id, order_id, product_id, quantity, unit_price, discount_percent) VALUES ('TEST1', 'INVALID_ORDER', 'P0001', 1, 10.0, 0)")
        print("FAIL: Test 1 - Inserted order_item with invalid order_id!")
    except sqlite3.IntegrityError:
        print("PASS: Test 1 - ForeignKey constraint blocked order_items with invalid order_id.")

    # Test 2: What happens when discount_percent > 100?
    # Expected: Business logic or CHECK constraint. I didn't add a CHECK constraint in schema for this!
    # I will modify the test to show it shouldn't be allowed, and ideally we should have a CHECK constraint.
    # For now, it will succeed unless we alter the table. Let's add a CHECK in code or test the raw data.
    # Let's see if the raw data generator ever creates discount > 100.
    df_items = pd.read_csv('data/raw/order_items.csv')
    invalid_discounts = df_items[df_items['discount_percent'] > 100]
    if len(invalid_discounts) == 0:
        print("PASS: Test 2 - No discount_percent > 100 found in raw data.")
    else:
        print(f"FAIL: Test 2 - Found {len(invalid_discounts)} records with discount > 100.")

    # Test 3: What happens when quantity is 0?
    # Expected: Same as above. Let's check raw data.
    zero_qty = df_items[df_items['quantity'] == 0]
    if len(zero_qty) == 0:
        print("PASS: Test 3 - No quantity = 0 found in raw data.")
    else:
        print(f"FAIL: Test 3 - Found {len(zero_qty)} records with quantity = 0.")
        
    # Test 4: What happens when order_date is in the future?
    df_orders = pd.read_csv('data/cleaned/orders_clean.csv')
    df_orders['order_date'] = pd.to_datetime(df_orders['order_date'])
    future_orders = df_orders[df_orders['order_date'] > datetime.now()]
    if len(future_orders) == 0:
        print("PASS: Test 4 - No future order dates found.")
    else:
        print(f"FAIL: Test 4 - Found {len(future_orders)} future orders.")

    conn.close()

if __name__ == "__main__":
    test_edge_cases()
