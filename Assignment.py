import pandas as pd


# 1. Load the CSV dataset
input_file = "Ecommerce_extracted/Combined_dataset.csv"
df = pd.read_csv(input_file)

print("Dataset loaded successfully")


# 2. Explore the dataset
print("\nFirst 5 rows:")
print(df.head())

print("\nLast 5 rows:")
print(df.tail())

print("\nNumber of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

print("\nColumn names:")
for column in df.columns:
    print(column)

print("\nData types:")
print(df.dtypes)


# 3. Check missing values
print("\nMissing values before cleaning:")
print(df.isnull().sum())


# 4. Start cleaning
df_clean = df.copy()

# Remove duplicate rows
duplicate_count = df_clean.duplicated().sum()
print("\nDuplicate rows before cleaning:", duplicate_count)

df_clean = df_clean.drop_duplicates()


# Fill missing values
df_clean["discount"] = df_clean["discount"].fillna(0)
df_clean["what_customers_said"] = df_clean["what_customers_said"].fillna("Not Available")
df_clean["seller_name"] = df_clean["seller_name"].fillna("Not Available")
df_clean["seller_information"] = df_clean["seller_information"].fillna("Not Available")
df_clean["variations"] = df_clean["variations"].fillna("Not Available")


# Replace hidden/redacted seller text that contains black block characters
black_block = chr(9608)

seller_name_hidden = df_clean["seller_name"].str.contains(black_block)
seller_info_hidden = df_clean["seller_information"].str.contains(black_block)

print("\nSeller names with black strips:", seller_name_hidden.sum())
print("Seller information with black strips:", seller_info_hidden.sum())

df_clean.loc[seller_name_hidden, "seller_name"] = "Not Available"
df_clean.loc[seller_info_hidden, "seller_information"] = "Not Available"


# Drop the videos column because most values are missing
df_clean = df_clean.drop("videos", axis=1)


# 5. Convert final_price into a numeric price column
df_clean["price"] = df_clean["final_price"].astype(str)
df_clean["price"] = df_clean["price"].str.replace('"', "", regex=False)
df_clean["price"] = df_clean["price"].str.replace(",", "", regex=False)

# The first character is the currency symbol, so we remove it
df_clean["price"] = df_clean["price"].str[1:]

df_clean["price"] = df_clean["price"].astype(float)


# 6. Create a derived column
# This dataset does not have a quantity column, so quantity is set to 1
df_clean["quantity"] = 1
df_clean["total_amount"] = df_clean["price"] * df_clean["quantity"]


# 6b. Clean and Expand Rating Details (amount_of_stars)
# The amount_of_stars column contains text in JSON format (e.g. {"1_star": 2, "2_stars": 0, ...})
# This is hard to analyze, so we convert it to separate numeric columns using json.loads
import json
stars_df = pd.json_normalize(df_clean["amount_of_stars"].apply(json.loads))

# Reset index to safely concatenate columns side-by-side
df_clean = df_clean.reset_index(drop=True)
df_clean = pd.concat([df_clean, stars_df], axis=1)


# 6c. Clean and Expand Product Details (product_details)
# The product_details column contains JSON strings with consistent keys: description, material_and_care, size_and_fit.
# We parse and extract these into three distinct text columns.
details_df = pd.json_normalize(df_clean["product_details"].apply(json.loads))

# Fill any missing values in the expanded details with 'Not Available'
details_df = details_df.fillna("Not Available")

# Concatenate these new detail columns to our main DataFrame
df_clean = pd.concat([df_clean, details_df], axis=1)


# 7. Basic operations
high_rated_products = df_clean[df_clean["rating"] >= 4.0]

print("\nHigh rated products:")
print(high_rated_products.head())

selected_columns = ["product_id", "title", "category", "price", "quantity", "total_amount", "rating", "5_stars", "description"]
small_table = df_clean[selected_columns]

print("\nSelected columns:")
print(small_table.head())


# 8. Check missing values after cleaning
print("\nMissing values after cleaning:")
print(df_clean.isnull().sum())


# 9. Save the cleaned dataset
output_file = "ecommerce_cleaned.csv"
df_clean.to_csv(output_file, index=False)

print("\nCleaned dataset saved as", output_file)
