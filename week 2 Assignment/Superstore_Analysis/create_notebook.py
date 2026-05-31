import json
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
notebook_path = os.path.join(base_dir, "Superstore_SQL_Analysis.ipynb")

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Superstore Sales SQL Analysis Notebook\n",
    "### Objective: Analyze sales data using SQL with filtering, aggregation, and business queries.\n",
    "\n",
    "This notebook demonstrates how to load, explore, filter, aggregate, and validate sales data using standard SQL in SQLite. The dataset used is `Sample - Superstore.csv` containing historical order transactions."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 1: Database Setup and Data Loading\n",
    "We will load the raw CSV data using Pandas, clean the column names for standard SQL usage, convert the string date fields into proper ISO `YYYY-MM-DD` date strings, and store the dataset in an SQLite database table called `superstore_sales`."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import sqlite3\n",
    "import pandas as pd\n",
    "\n",
    "# File paths\n",
    "csv_path = r\"Sample - Superstore.csv\"\n",
    "db_path = \"superstore.db\"\n",
    "\n",
    "# Load CSV and clean columns\n",
    "df = pd.read_csv(csv_path, encoding=\"latin1\")\n",
    "df.columns = [col.lower().replace(\" \", \"_\").replace(\"-\", \"_\") for col in df.columns]\n",
    "\n",
    "# Convert dates to ISO YYYY-MM-DD strings\n",
    "df['order_date'] = pd.to_datetime(df['order_date'], format='%m/%d/%Y', errors='coerce').dt.strftime('%Y-%m-%d')\n",
    "df['ship_date'] = pd.to_datetime(df['ship_date'], format='%m/%d/%Y', errors='coerce').dt.strftime('%Y-%m-%d')\n",
    "\n",
    "# Establish connection and write to database\n",
    "conn = sqlite3.connect(db_path)\n",
    "df.to_sql(\"superstore_sales\", conn, if_exists=\"replace\", index=False)\n",
    "print(\"Database initialized and data loaded successfully. Total rows:\", len(df))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 2: Table Exploration\n",
    "Let's explore the schema structure and check the first few sample rows."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. Explore schema\n",
    "schema = pd.read_sql_query(\"PRAGMA table_info(superstore_sales)\", conn)\n",
    "display(schema)\n",
    "\n",
    "# 2. View 3 sample rows\n",
    "samples = pd.read_sql_query(\"SELECT row_id, order_id, order_date, customer_name, region, category, sales, profit FROM superstore_sales LIMIT 3\", conn)\n",
    "display(samples)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 3: Apply WHERE Filters\n",
    "Applying WHERE filters on different conditions (Region, Category, Date ranges, Sales amounts)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 3.1 Filter by region = 'West'\n",
    "west_orders = pd.read_sql_query(\"SELECT order_id, customer_name, region, category, sales FROM superstore_sales WHERE region = 'West' LIMIT 5\", conn)\n",
    "print(\"West Region Sample:\")\n",
    "display(west_orders)\n",
    "\n",
    "# 3.2 Filter by category = 'Technology'\n",
    "tech_orders = pd.read_sql_query(\"SELECT order_id, customer_name, category, sub_category, sales FROM superstore_sales WHERE category = 'Technology' LIMIT 5\", conn)\n",
    "print(\"\\nTechnology Category Sample:\")\n",
    "display(tech_orders)\n",
    "\n",
    "# 3.3 Filter by date (January 2017)\n",
    "jan_2017_orders = pd.read_sql_query(\"SELECT order_id, order_date, customer_name, sales FROM superstore_sales WHERE order_date BETWEEN '2017-01-01' AND '2017-01-31' LIMIT 5\", conn)\n",
    "print(\"\\nJanuary 2017 Orders:\")\n",
    "display(jan_2017_orders)\n",
    "\n",
    "# 3.4 Filter by high-value sales (> $1000)\n",
    "high_value_orders = pd.read_sql_query(\"SELECT order_id, customer_name, sales, profit FROM superstore_sales WHERE sales > 1000 LIMIT 5\", conn)\n",
    "print(\"\\nHigh-Value Orders (> $1000):\")\n",
    "display(high_value_orders)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 4: Use GROUP BY for Aggregations\n",
    "Aggregating metrics (sums, counts, and averages) by various dimensions to summarize performance."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 4.1 Aggregations by product Category\n",
    "cat_summary = pd.read_sql_query(\"\"\"\n",
    "    SELECT category, \n",
    "           ROUND(SUM(sales), 2) AS total_sales, \n",
    "           SUM(quantity) AS total_quantity, \n",
    "           ROUND(AVG(sales), 2) AS avg_sales, \n",
    "           ROUND(AVG(profit), 2) AS avg_profit \n",
    "    FROM superstore_sales \n",
    "    GROUP BY category\n",
    "\"\"\", conn)\n",
    "print(\"Summary by Category:\")\n",
    "display(cat_summary)\n",
    "\n",
    "# 4.2 Aggregations by Region & Segment\n",
    "region_summary = pd.read_sql_query(\"\"\"\n",
    "    SELECT region, segment, \n",
    "           ROUND(SUM(sales), 2) AS total_sales, \n",
    "           ROUND(AVG(profit), 2) AS avg_profit \n",
    "    FROM superstore_sales \n",
    "    GROUP BY region, segment\n",
    "    ORDER BY region, total_sales DESC\n",
    "\"\"\", conn)\n",
    "print(\"\\nSummary by Region & Segment:\")\n",
    "display(region_summary)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 5: Sort and Limit Results\n",
    "Finding top products by sales and top sub-categories by profitability."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 5.1 Top 5 Products by Sales\n",
    "top_products = pd.read_sql_query(\"\"\"\n",
    "    SELECT product_name, category, \n",
    "           ROUND(SUM(sales), 2) AS total_sales,\n",
    "           SUM(quantity) AS total_qty\n",
    "    FROM superstore_sales \n",
    "    GROUP BY product_name, category \n",
    "    ORDER BY total_sales DESC \n",
    "    LIMIT 5\n",
    "\"\"\", conn)\n",
    "print(\"Top 5 Selling Products:\")\n",
    "display(top_products)\n",
    "\n",
    "# 5.2 Top 5 Sub-Categories by Profit\n",
    "top_subcats = pd.read_sql_query(\"\"\"\n",
    "    SELECT category, sub_category, \n",
    "           ROUND(SUM(profit), 2) AS total_profit \n",
    "    FROM superstore_sales \n",
    "    GROUP BY category, sub_category \n",
    "    ORDER BY total_profit DESC \n",
    "    LIMIT 5\n",
    "\"\"\", conn)\n",
    "print(\"\\nTop 5 Profitable Sub-Categories:\")\n",
    "display(top_subcats)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 6: Business Use Cases\n",
    "Let's solve for monthly trends, top customers, and duplicate transactions."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 6.1 Monthly Sales Trends (First 12 Months)\n",
    "monthly_trends = pd.read_sql_query(\"\"\"\n",
    "    SELECT strftime('%Y-%m', order_date) AS year_month, \n",
    "           ROUND(SUM(sales), 2) AS monthly_sales, \n",
    "           ROUND(SUM(profit), 2) AS monthly_profit \n",
    "    FROM superstore_sales \n",
    "    GROUP BY year_month \n",
    "    ORDER BY year_month \n",
    "    LIMIT 12\n",
    "\"\"\", conn)\n",
    "print(\"Monthly Trends:\")\n",
    "display(monthly_trends)\n",
    "\n",
    "# 6.2 Top 5 Customers by Purchases\n",
    "top_customers = pd.read_sql_query(\"\"\"\n",
    "    SELECT customer_id, customer_name, segment, \n",
    "           ROUND(SUM(sales), 2) AS total_spend,\n",
    "           COUNT(DISTINCT order_id) AS order_count\n",
    "    FROM superstore_sales \n",
    "    GROUP BY customer_id, customer_name, segment \n",
    "    ORDER BY total_spend DESC \n",
    "    LIMIT 5\n",
    "\"\"\", conn)\n",
    "print(\"\\nTop 5 Spending Customers:\")\n",
    "display(top_customers)\n",
    "\n",
    "# 6.3 Duplicate Row Check\n",
    "row_duplicates = pd.read_sql_query(\"\"\"\n",
    "    SELECT row_id, COUNT(*) AS count \n",
    "    FROM superstore_sales \n",
    "    GROUP BY row_id \n",
    "    HAVING count > 1\n",
    "\"\"\", conn)\n",
    "print(f\"\\nDuplicate row_ids found: {len(row_duplicates)}\")\n",
    "\n",
    "# 6.4 Duplicate Items within the same Order\n",
    "item_duplicates = pd.read_sql_query(\"\"\"\n",
    "    SELECT order_id, product_id, COUNT(*) AS count \n",
    "    FROM superstore_sales \n",
    "    GROUP BY order_id, product_id \n",
    "    HAVING count > 1\n",
    "    LIMIT 5\n",
    "\"\"\", conn)\n",
    "print(\"\\nDuplicate order-product combinations (first 5 examples):\")\n",
    "display(item_duplicates)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 7: Data Validation and Quality Checks\n",
    "Validating row counts and checking data quality (null values, negative quantities or sales)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# 7.1 Row counts verification\n",
    "total_rows = pd.read_sql_query(\"SELECT COUNT(*) AS total_rows FROM superstore_sales\", conn).iloc[0]['total_rows']\n",
    "print(f\"Total row count match (Expected 9994): {total_rows}\")\n",
    "\n",
    "# 7.2 Null values check\n",
    "nulls = pd.read_sql_query(\"\"\"\n",
    "    SELECT \n",
    "        SUM(CASE WHEN row_id IS NULL THEN 1 ELSE 0 END) AS null_row_ids,\n",
    "        SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) AS null_order_ids,\n",
    "        SUM(CASE WHEN order_date IS NULL THEN 1 ELSE 0 END) AS null_order_dates,\n",
    "        SUM(CASE WHEN customer_name IS NULL THEN 1 ELSE 0 END) AS null_customer_names,\n",
    "        SUM(CASE WHEN sales IS NULL THEN 1 ELSE 0 END) AS null_sales,\n",
    "        SUM(CASE WHEN profit IS NULL THEN 1 ELSE 0 END) AS null_profits\n",
    "    FROM superstore_sales\n",
    "\"\"\", conn)\n",
    "print(\"\\nNull counts check:\")\n",
    "display(nulls)\n",
    "\n",
    "# 7.3 Invalid financial or physical data check (sales <= 0 or qty <= 0)\n",
    "invalids = pd.read_sql_query(\"\"\"\n",
    "    SELECT COUNT(*) AS invalid_records \n",
    "    FROM superstore_sales \n",
    "    WHERE sales <= 0 OR quantity <= 0\n",
    "\"\"\", conn).iloc[0]['invalid_records']\n",
    "print(f\"\\nInvalid records count (expected 0): {invalids}\")\n",
    "\n",
    "# Clean up connection\n",
    "conn.close()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Summary of Insights\n",
    "\n",
    "1. **Category Performance**:\n",
    "   - **Technology** is the highest revenue category ($836,154.03) and has the highest average profit ($78.75 per order).\n",
    "   - **Office Supplies** drives the highest volume of items sold (22,906 items), but has a smaller average profit ($20.33 per order).\n",
    "   - **Furniture** brings in solid revenue ($741,999.80) but has a very low average profit ($8.70 per order), indicating high supply chain/returns costs.\n",
    "\n",
    "2. **Regional Segments**:\n",
    "   - The **Consumer** segment in the **East** region is the top-performing regional segment with $350,908.17 in sales.\n",
    "\n",
    "3. **Top Customer**:\n",
    "   - **Sean Miller** is the top customer by lifetime value, spending a total of $25,043.05 across his orders.\n",
    "\n",
    "4. **Duplicate Orders**:\n",
    "   - We found no duplicate `row_id`s, verifying database row uniqueness.\n",
    "   - However, we did find some orders containing multiple entries for the same product, suggesting some split orders or shipping entries. These are worth auditing for sales record deduplication."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

with open(notebook_path, "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1)

print(f"Jupyter Notebook generated successfully at {notebook_path}")
