import os
import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

def generate_data():
    fake = Faker()
    Faker.seed(42)
    random.seed(42)

    # Directories
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/cleaned', exist_ok=True)

    # 1. Customers
    num_customers = 600
    customer_types = ['REGULAR', 'PREMIUM', 'VIP']
    
    customers = []
    for i in range(1, num_customers + 1):
        c_id = f"C{i:04d}"
        name = fake.name()
        
        # 2% invalid emails (missing @ or domain)
        is_invalid_email = random.random() < 0.02
        if is_invalid_email:
            email_choice = random.choice([fake.user_name(), f"{fake.user_name()}@"])
            email = email_choice
        else:
            email = fake.email()
            
        reg_date = fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
        c_type = random.choices(customer_types, weights=[0.7, 0.2, 0.1])[0]
        
        customers.append([c_id, name, email, reg_date, c_type])
        
    df_customers = pd.DataFrame(customers, columns=['customer_id', 'customer_name', 'email', 'registration_date', 'customer_type'])
    df_customers.to_csv('data/raw/customers.csv', index=False)

    # 2. Products
    num_products = 200
    categories = {
        'Electronics': ['Laptops', 'Smartphones', 'Audio', 'Accessories'],
        'Clothing': ['Men', 'Women', 'Kids', 'Shoes'],
        'Home': ['Furniture', 'Decor', 'Kitchen', 'Bedding'],
        'Books': ['Fiction', 'Non-Fiction', 'Educational', 'Comics']
    }
    
    products = []
    for i in range(1, num_products + 1):
        p_id = f"P{i:04d}"
        cat = random.choice(list(categories.keys()))
        subcat = random.choice(categories[cat])
        
        # extra spaces or mixed case for some
        base_name = f"{fake.word()} {fake.word()} {subcat}"
        should_mess_name = random.random() < 0.15
        if should_mess_name:
            if random.random() < 0.5:
                # extra spaces
                name = f"  {base_name}   "
            else:
                # mixed case
                name = "".join(random.choice([k.upper(), k.lower()]) for k in base_name)
        else:
            name = base_name.title()
            
        cost_price = round(random.uniform(5.0, 500.0), 2)
        products.append([p_id, name, cat, subcat, cost_price])
        
    df_products = pd.DataFrame(products, columns=['product_id', 'product_name', 'category', 'subcategory', 'cost_price'])
    df_products.to_csv('data/raw/products.csv', index=False)

    # 3. Orders
    num_orders = 1000
    statuses = ['PLACED', 'SHIPPED', 'DELIVERED', 'CANCELLED', 'RETURNED']
    regions = ['NA', 'EU', 'AS', 'SA', 'AF', 'OC']
    
    orders = []
    for i in range(1, num_orders + 1):
        o_id = f"O{i:05d}"
        
        # 5% NULL customer_id
        is_null_customer = random.random() < 0.05
        c_id = None if is_null_customer else random.choice(df_customers['customer_id'])
        
        # Wrong format order_date (DD-MM-YYYY)
        is_wrong_format = random.random() < 0.10
        raw_date = fake.date_time_between(start_date='-1y', end_date='now')
        if is_wrong_format:
            o_date = raw_date.strftime('%d-%m-%Y')
        else:
            o_date = raw_date.strftime('%Y-%m-%d %H:%M:%S')
            
        status = random.choices(statuses, weights=[0.1, 0.2, 0.6, 0.05, 0.05])[0]
        region = random.choice(regions)
        
        orders.append([o_id, c_id, o_date, status, region])
        
    df_orders = pd.DataFrame(orders, columns=['order_id', 'customer_id', 'order_date', 'status', 'region_code'])
    df_orders.to_csv('data/raw/orders.csv', index=False)

    # 4. Order Items
    num_order_items = 2500
    order_items = []
    
    valid_order_ids = df_orders['order_id'].tolist()
    
    for i in range(1, num_order_items + 1):
        item_id = f"I{i:05d}"
        
        # Reference valid order_ids
        o_id = random.choice(valid_order_ids)
        p_id = random.choice(df_products['product_id'])
        
        # 3% negative quantity
        is_negative_qty = random.random() < 0.03
        if is_negative_qty:
            qty = -1 * random.randint(1, 5)
        else:
            qty = random.randint(1, 5)
            
        # Get product base cost to make unit price sensible
        p_cost = df_products[df_products['product_id'] == p_id]['cost_price'].iloc[0]
        unit_price = round(p_cost * random.uniform(1.2, 2.5), 2)
        
        discount_percent = random.choice([0, 0, 0, 5, 10, 15, 20])
        
        order_items.append([item_id, o_id, p_id, qty, unit_price, discount_percent])
        
    # Introduce one edge case where order_items references a non-existent order
    order_items.append([f"I{num_order_items+1:05d}", "O99999", random.choice(df_products['product_id']), 1, 50.0, 0])

    df_order_items = pd.DataFrame(order_items, columns=['item_id', 'order_id', 'product_id', 'quantity', 'unit_price', 'discount_percent'])
    df_order_items.to_csv('data/raw/order_items.csv', index=False)

    print("Data generation complete! Files saved to data/raw/")

if __name__ == "__main__":
    generate_data()
