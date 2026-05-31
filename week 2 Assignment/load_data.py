import os
import sqlite3
import pandas as pd

# Define paths
csv_path = r"c:\Users\Palak\Desktop\SQL Basics\Sample - Superstore.csv"
output_dir = r"c:\Users\Palak\Desktop\SQL Basics\Superstore_Analysis"
db_path = os.path.join(output_dir, "superstore.db")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load CSV
print("Loading CSV...")
df = pd.read_csv(csv_path, encoding="latin1")

# Clean column names for cleaner SQL (convert spaces and hyphens to underscores, lowercase)
df.columns = [col.lower().replace(" ", "_").replace("-", "_") for col in df.columns]

# Print columns to verify
print("Cleaned Columns:", df.columns.tolist())

# Load into SQLite database
print(f"Creating SQLite DB at {db_path}...")
conn = sqlite3.connect(db_path)
df.to_sql("superstore_sales", conn, if_exists="replace", index=False)

print("Data loaded. Verifying row count...")
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM superstore_sales")
count = cursor.fetchone()[0]
print(f"Total rows in superstore_sales table: {count}")

# Close connection
conn.close()
print("Setup complete.")
