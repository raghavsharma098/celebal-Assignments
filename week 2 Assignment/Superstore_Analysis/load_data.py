import os
import sqlite3
import pandas as pd

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(base_dir, "Sample - Superstore.csv")
db_path = os.path.join(base_dir, "superstore.db")

print("Loading CSV...")
df = pd.read_csv(csv_path, encoding="latin1")

df.columns = [col.lower().replace(" ", "_").replace("-", "_") for col in df.columns]

print("Formatting date columns...")
df['order_date'] = pd.to_datetime(df['order_date'], format='%m/%d/%Y', errors='coerce').dt.strftime('%Y-%m-%d')
df['ship_date'] = pd.to_datetime(df['ship_date'], format='%m/%d/%Y', errors='coerce').dt.strftime('%Y-%m-%d')

print("Sample date values:")
print(df[['order_date', 'ship_date']].head(5))

print(f"Creating SQLite DB at {db_path}...")
conn = sqlite3.connect(db_path)
df.to_sql("superstore_sales", conn, if_exists="replace", index=False)

print("Data loaded and date columns formatted to standard SQL format.")
conn.close()
