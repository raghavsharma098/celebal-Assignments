import os
import pandas as pd

base_dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(base_dir, "Sample - Superstore.csv"), encoding="latin1")
print("Columns:")
print(df.columns.tolist())
print("\nShape:", df.shape)
print("\nSample Data:")
print(df.head(2).to_dict(orient="records"))
