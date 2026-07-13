import os
import pandas as pd
import re

def clean_orders(df):
    """Fix date formats, handle NULL customer_ids"""
    issues_found = {}
    
    # Check NULL customer_ids
    null_customers = df['customer_id'].isna().sum()
    issues_found['null_customer_ids'] = null_customers
    
    # Handle NULLs (e.g., fill with 'UNKNOWN' or drop. We will fill with 'UNKNOWN')
    df['customer_id'] = df['customer_id'].fillna('UNKNOWN')
    
    # Fix date formats
    # Dates can be 'YYYY-MM-DD HH:MM:SS' or 'DD-MM-YYYY'
    # We will standardize to 'YYYY-MM-DD HH:MM:SS'
    
    def parse_date(date_str):
        try:
            return pd.to_datetime(date_str, format='%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                # DD-MM-YYYY
                return pd.to_datetime(date_str, format='%d-%m-%Y')
            except ValueError:
                return pd.NaT

    original_dates = df['order_date'].copy()
    df['order_date'] = df['order_date'].apply(parse_date)
    
    # Find how many were modified (which means they were probably DD-MM-YYYY)
    # Actually, simpler: check how many match the DD-MM-YYYY regex
    wrong_format_count = original_dates.str.match(r'^\d{2}-\d{2}-\d{4}$').sum()
    issues_found['wrong_date_formats_fixed'] = wrong_format_count
    
    return df, issues_found

def clean_products(df):
    """Normalize product names (trim spaces, title case)"""
    issues_found = {}
    
    original_names = df['product_name'].copy()
    
    # Clean: strip spaces, convert to title case
    # Convert all multiple spaces to single space, strip, then title case
    df['product_name'] = df['product_name'].apply(lambda x: re.sub(r'\s+', ' ', str(x)).strip().title())
    
    changed_count = (original_names != df['product_name']).sum()
    issues_found['product_names_normalized'] = changed_count
    
    return df, issues_found

def validate_emails(df):
    """Return list of customer_ids with invalid emails"""
    # Valid email regex (simple)
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    invalid_mask = ~df['email'].str.match(pattern, na=False)
    
    invalid_ids = df[invalid_mask]['customer_id'].tolist()
    return invalid_ids

def check_referential_integrity(df_order_items, df_orders):
    """Find order_items that reference non-existent orders"""
    valid_order_ids = set(df_orders['order_id'].dropna())
    
    invalid_items = df_order_items[~df_order_items['order_id'].isin(valid_order_ids)]
    return invalid_items

def main():
    print("Starting data cleaning process...")
    
    # Read raw data
    try:
        df_customers = pd.read_csv('data/raw/customers.csv')
        df_products = pd.read_csv('data/raw/products.csv')
        # keep_default_na=False prevents 'NA' (North America) from becoming NaN
        df_orders = pd.read_csv('data/raw/orders.csv', keep_default_na=False, na_values=[''])
        df_order_items = pd.read_csv('data/raw/order_items.csv')
    except FileNotFoundError:
        print("Raw data files not found. Please run generate_data.py first.")
        return

    report = []

    # 1. Clean Orders
    df_orders_clean, order_issues = clean_orders(df_orders)
    report.append(f"Orders cleaned. NULL customer_ids handled: {order_issues['null_customer_ids']}. Wrong date formats fixed: {order_issues['wrong_date_formats_fixed']}.")

    # 2. Clean Products
    df_products_clean, product_issues = clean_products(df_products)
    report.append(f"Products cleaned. Names normalized: {product_issues['product_names_normalized']}.")

    # 3. Validate Emails
    invalid_emails_ids = validate_emails(df_customers)
    report.append(f"Customer emails validated. Found {len(invalid_emails_ids)} invalid emails.")
    # Clean up invalid emails by setting to UNKNOWN (or could drop them, depending on requirements, let's keep them and flag)
    # The requirement is just to return list and report, but let's leave them or fix them. We will just report.

    # 4. Check Referential Integrity
    invalid_order_items = check_referential_integrity(df_order_items, df_orders_clean)
    report.append(f"Referential integrity checked. Found {len(invalid_order_items)} order_items referencing non-existent orders.")
    
    # Fix referential integrity by dropping invalid items
    if len(invalid_order_items) > 0:
        df_order_items_clean = df_order_items[~df_order_items['item_id'].isin(invalid_order_items['item_id'])]
        report.append(f"Dropped {len(invalid_order_items)} invalid order_items.")
    else:
        df_order_items_clean = df_order_items.copy()

    # Also fix negative quantity in order_items (was mentioned in generation but we should clean it)
    negative_qty = (df_order_items_clean['quantity'] < 0).sum()
    report.append(f"Found {negative_qty} order_items with negative quantity (returns). Kept in dataset as they represent returns.")
    
    # Save cleaned data
    os.makedirs('data/cleaned', exist_ok=True)
    df_customers.to_csv('data/cleaned/customers_clean.csv', index=False)
    df_products_clean.to_csv('data/cleaned/products_clean.csv', index=False)
    df_orders_clean.to_csv('data/cleaned/orders_clean.csv', index=False)
    df_order_items_clean.to_csv('data/cleaned/order_items_clean.csv', index=False)
    
    print("\n--- CLEANING REPORT ---")
    for r in report:
        print(r)
    print("-----------------------")
    print("Cleaned data saved to data/cleaned/")

if __name__ == "__main__":
    main()
