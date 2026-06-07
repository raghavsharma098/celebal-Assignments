import os
import sqlite3
import pandas as pd

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "Sample - Superstore.csv")
db_path = os.path.join(base_dir, "superstore.db")

print("Reading the Superstore CSV...")
df = pd.read_csv(csv_path, encoding="latin1")
df.columns = [c.lower().replace(" ", "_").replace("-", "_") for c in df.columns]

df["order_date"] = pd.to_datetime(df["order_date"], format="%m/%d/%Y", errors="coerce").dt.strftime("%Y-%m-%d")
df["ship_date"] = pd.to_datetime(df["ship_date"], format="%m/%d/%Y", errors="coerce").dt.strftime("%Y-%m-%d")

print(f"Loading {len(df):,} rows into superstore_raw...")
conn = sqlite3.connect(db_path)
df.to_sql("superstore_raw", conn, if_exists="replace", index=False)

cur = conn.cursor()

cur.executescript(
    """
    DROP TABLE IF EXISTS customers;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS products;

    CREATE TABLE customers (
        customer_id   TEXT PRIMARY KEY,
        customer_name TEXT,
        segment       TEXT
    );

    CREATE TABLE products (
        product_id   TEXT PRIMARY KEY,
        category     TEXT,
        sub_category TEXT,
        product_name TEXT
    );

    CREATE TABLE orders (
        row_id      INTEGER PRIMARY KEY,
        order_id    TEXT,
        order_date  TEXT,
        ship_date   TEXT,
        ship_mode   TEXT,
        customer_id TEXT,
        product_id  TEXT,
        region      TEXT,
        city        TEXT,
        state       TEXT,
        sales       REAL,
        quantity    INTEGER,
        discount    REAL,
        profit      REAL
    );
    """
)

print("Populating customers, products and orders with SELECT DISTINCT...")
cur.executescript(
    """
    INSERT INTO customers
    SELECT DISTINCT customer_id, customer_name, segment
    FROM superstore_raw;

    INSERT INTO products
    SELECT product_id, MIN(category), MIN(sub_category), MIN(product_name)
    FROM superstore_raw
    GROUP BY product_id;

    INSERT INTO orders
    SELECT DISTINCT row_id, order_id, order_date, ship_date, ship_mode,
                    customer_id, product_id, region, city, state,
                    sales, quantity, discount, profit
    FROM superstore_raw;
    """
)

conn.commit()

for t in ["superstore_raw", "customers", "products", "orders"]:
    n = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"  {t:<15} {n:,} rows")

conn.close()
print(f"Done. Database written to {db_path}")
