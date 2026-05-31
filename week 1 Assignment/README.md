# Python-data-cleaning-assignment

# Ecommerce Data Cleaning with Pandas

## Assignment Objective

The objective of this assignment is to learn Python basics and perform basic data exploration and cleaning using Pandas.

In this project, I worked on an ecommerce dataset and used Pandas to load, explore, clean, transform, and save the final cleaned dataset.

This project helped me understand how real-world datasets are usually messy and need cleaning before analysis.

---

## Dataset Used

The dataset used in this project is:

```text
Combined_dataset.csv
```

It contains ecommerce product-related information such as product title, price, discount, rating, seller details, customer reviews, product details, and star ratings.

---

## Dataset Overview

| Metric | Original Dataset | Cleaned Dataset |
| --- | --- | --- |
| Row Count | 1000 rows | 1000 rows |
| Column Count | 24 columns | 34 columns |
| Duplicates | 0 | 0 |
| Missing Values | 2639 missing values | 0 missing values |

---

## Tools and Libraries Used

- Python
- Pandas
- Jupyter Notebook
- CSV file handling
- JSON handling

---

## Steps Performed

---

## 1. Loaded the CSV Dataset

First, I loaded the ecommerce dataset into a Pandas DataFrame using `pd.read_csv()`.

```python
import pandas as pd

df = pd.read_csv("Ecommerce_extracted/Combined_dataset.csv")
```

This step helped me import the CSV file into Python so that I could perform data exploration and cleaning using Pandas.

---

## 2. Explored the Dataset

After loading the dataset, I explored it to understand its structure, columns, data types, and basic information.

I used the following Pandas functions:

```python
# Display the first 5 rows of the dataset
df.head()
```

```python
# Display the last 5 rows of the dataset
df.tail()
```

```python
# Check the number of rows and columns
df.shape
```

```python
# Display all column names
df.columns
```

```python
# Check data types of each column
df.dtypes
```

```python
# Get complete information about the dataset
df.info()
```

```python
# Get statistical summary of numerical columns
df.describe()
```

These commands helped me understand:

- What the dataset looks like
- How many rows and columns are present
- What columns are available in the dataset
- Which columns contain text, numbers, or other data types
- Basic statistical details of numerical columns

---

## 3. Checked and Handled Missing Values

I checked missing values in the dataset using `isnull().sum()`.

```python
# Check missing values in each column
df.isnull().sum()
```

The original dataset had missing values in several columns. Missing values can create problems during analysis, so I handled them based on the type of column.

First, I created a copy of the original dataset so the original data would remain safe.

```python
# Create a copy of the original dataset
df_clean = df.copy()
```

I filled missing values in the `discount` column with `0`.

```python
# Fill missing discount values with 0
df_clean["discount"] = df_clean["discount"].fillna(0)
```

For text columns, I filled missing values with `"Not Available"`.

```python
# Fill missing text values with "Not Available"
text_columns = df_clean.select_dtypes(include="object").columns

for col in text_columns:
    df_clean[col] = df_clean[col].fillna("Not Available")
```

The `videos` column had too many missing values, so I removed it from the dataset.

```python
# Drop videos column because it had too many missing values
df_clean = df_clean.drop("videos", axis=1)
```

I also replaced black block characters like `███` in seller names with `"Not Available"`.

```python
# Replace black block characters in seller_name
df_clean["seller_name"] = df_clean["seller_name"].astype(str).str.replace("███", "Not Available")
```

After handling missing values, I checked again to make sure there were no missing values left.

```python
# Check missing values again after cleaning
df_clean.isnull().sum()
```

---

## 4. Removed Duplicate Rows

Duplicate rows can affect analysis because the same data may be counted more than once.

I checked duplicate rows using:

```python
# Check duplicate rows
df_clean.duplicated().sum()
```

There were no duplicate rows in this dataset, but I still used the duplicate removal step to keep the dataset clean.

```python
# Remove duplicate rows
df_clean = df_clean.drop_duplicates()
```

This step ensured that every row in the dataset was unique.

---

## 5. Converted Price Data

The `final_price` column contained price values in text format.

Example:

```text
₹3,995.00
```

Since this value was stored as text, it could not be directly used for calculations. So, I cleaned the price column and converted it into a numeric value.

```python
# Convert final_price column into numeric price column
df_clean["price"] = df_clean["final_price"].astype(str).str.replace('"', '').str.replace(',', '')
df_clean["price"] = df_clean["price"].str[1:].astype(float)
```

In this step:

- Extra quotes were removed
- Commas were removed
- Currency symbol was removed
- The value was converted into float

After this, the new `price` column could be used for calculations.

---

## 6. Created a Derived Column

The assignment required creating a new column using this formula:

```text
total_amount = price * quantity
```

Since the dataset did not already have a `quantity` column, I created one and set its value to `1`.

```python
# Create quantity column
df_clean["quantity"] = 1
```

Then I created the `total_amount` column.

```python
# Create total_amount column
df_clean["total_amount"] = df_clean["price"] * df_clean["quantity"]
```

This new column shows the total amount for each product.

---

## 7. Cleaned JSON Columns

Some columns in the dataset contained dictionary or JSON-like data.

Examples:

- `amount_of_stars`
- `product_details`

These columns were difficult to read directly, so I split them into separate useful columns.

First, I imported the JSON library.

```python
import json
```

Then I cleaned and normalized the `amount_of_stars` column.

```python
# Convert amount_of_stars column from JSON-like text to separate columns
stars_data = df_clean["amount_of_stars"].apply(lambda x: json.loads(x.replace("'", '"')) if isinstance(x, str) and x.startswith("{") else {})

stars_df = pd.json_normalize(stars_data)

df_clean = pd.concat([df_clean, stars_df], axis=1)
```

This created separate columns such as:

- `1_star`
- `2_stars`
- `3_stars`
- `4_stars`
- `5_stars`

Then I cleaned and normalized the `product_details` column.

```python
# Convert product_details column from JSON-like text to separate columns
details_data = df_clean["product_details"].apply(lambda x: json.loads(x.replace("'", '"')) if isinstance(x, str) and x.startswith("{") else {})

details_df = pd.json_normalize(details_data)

df_clean = pd.concat([df_clean, details_df], axis=1)
```

This created separate columns such as:

- `description`
- `material_and_care`
- `size_and_fit`

This made the dataset easier to understand and analyze.

---

## 8. Performed Basic Operations

I performed basic Pandas operations such as filtering rows and selecting columns.

First, I filtered products with a rating greater than or equal to `4.0`.

```python
# Filter products with rating greater than or equal to 4.0
high_rated = df_clean[df_clean["rating"] >= 4.0]
```

This helped me find highly rated products.

Then, I selected some important columns to create a smaller table for viewing.

```python
# Select important columns
selected_cols = ["product_id", "title", "price", "rating", "5_stars", "description"]

small_table = df_clean[selected_cols]
```

This helped me focus only on the most useful columns.

---

## 9. Saved the Cleaned Dataset

After cleaning and transforming the dataset, I saved the final cleaned dataset into a new CSV file.

```python
# Save cleaned dataset
df_clean.to_csv("ecommerce_cleaned.csv", index=False)
```

The cleaned dataset was saved as:

```text
ecommerce_cleaned.csv
```

I used `index=False` so that Pandas would not add an extra index column in the CSV file.

---

## Final Output

The final output of this assignment includes:

- Jupyter Notebook file
- Original dataset
- Cleaned dataset
- README file
- Brief summary

---

## Project Files

```text
Ecommerce-Data-Cleaning-with-Pandas/
|
|-- Ecommerce_Data_Cleaning.ipynb
|-- Assignemt.py
|-- Combined_dataset.csv
|-- ecommerce_cleaned.csv
|-- README.md
```

---

## Brief Summary

In this assignment, I used Python Pandas to perform basic data exploration and cleaning on an ecommerce dataset.

I loaded the dataset, checked its structure, identified missing values, handled missing data, removed duplicate rows, converted price values into numeric format, created a new `total_amount` column, cleaned JSON-like columns, and saved the final cleaned dataset as a new CSV file.

This assignment improved my understanding of how to clean real-world data and prepare it for further analysis.

---

## Conclusion

This project shows how Pandas can be used for basic data cleaning and exploration.

By completing this assignment, I learned how to:

- Load a CSV dataset
- Explore rows, columns, and data types
- Handle missing values
- Remove duplicate rows
- Convert text-based price values into numbers
- Create new derived columns
- Clean JSON-like columns
- Save the cleaned dataset as a new CSV file

Overall, this assignment helped me understand the complete basic workflow of data cleaning using Pandas.
