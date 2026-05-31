import pandas as pd

# Load the first few rows of the CSV to inspect columns and data types
df = pd.read_csv(r"c:\Users\Palak\Desktop\SQL Basics\Sample - Superstore.csv", encoding="latin1")
print("Columns:")
print(df.columns.tolist())
print("\nShape:", df.shape)
print("\nSample Data:")
print(df.head(2).to_dict(orient="records"))
