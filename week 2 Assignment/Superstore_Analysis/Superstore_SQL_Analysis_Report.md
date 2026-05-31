# Superstore Sales SQL Analysis Report
**Junior Data Analyst Project — Part 2**

---

## 📌 Executive Summary
This report analyzes transaction-level sales data for **Superstore** using standard SQL. The analysis is performed on an SQLite database constructed from the raw `Sample - Superstore.csv` dataset, which contains **9,994 rows** across **21 columns** mapping historical orders from 2014 to 2017.

All code and assets for this analysis are saved in the dedicated directory:
[Superstore_Analysis](file:///c:/Users/Palak/Desktop/SQL%20Basics/Superstore_Analysis/)

### Key Documents Created:
* [SQL Script File](file:///c:/Users/Palak/Desktop/SQL%20Basics/Superstore_Analysis/Superstore_SQL_Analysis.sql) — Clean, formatted, and fully-commented SQL code.
* [Jupyter Notebook](file:///c:/Users/Palak/Desktop/SQL%20Basics/Superstore_Analysis/Superstore_SQL_Analysis.ipynb) — Executable notebook integrating code, SQL queries, interactive outputs, and step-by-step documentation.
* [SQLite Database](file:///c:/Users/Palak/Desktop/SQL%20Basics/Superstore_Analysis/superstore.db) — The local SQLite relational database containing the cleaned data.

---

## 🛠️ Step 1: Database Loading and Date Standardisation
To support clean SQL querying and index optimization, the raw CSV columns were mapped to standard **snake_case** database format. Date fields (`Order Date` and `Ship Date`) were converted from string representation (`M/D/YYYY`) to standard ISO dates (`YYYY-MM-DD`) during loading.

---

## 🔍 Step 2: Table Exploration

### Schema Definition
```sql
PRAGMA table_info(superstore_sales);
```
| CID | Name | Type | NotNull | Default | PK |
|---|---|---|---|---|---|
| 0 | `row_id` | INTEGER | 0 | None | 0 |
| 1 | `order_id` | TEXT | 0 | None | 0 |
| 2 | `order_date` | TEXT (ISO) | 0 | None | 0 |
| 3 | `ship_date` | TEXT (ISO) | 0 | None | 0 |
| 4 | `ship_mode` | TEXT | 0 | None | 0 |
| 5 | `customer_id` | TEXT | 0 | None | 0 |
| 6 | `customer_name` | TEXT | 0 | None | 0 |
| 7 | `segment` | TEXT | 0 | None | 0 |
| 8 | `country` | TEXT | 0 | None | 0 |
| 9 | `city` | TEXT | 0 | None | 0 |
| 10 | `state` | TEXT | 0 | None | 0 |
| 11 | `postal_code` | INTEGER | 0 | None | 0 |
| 12 | `region` | TEXT | 0 | None | 0 |
| 13 | `product_id` | TEXT | 0 | None | 0 |
| 14 | `category` | TEXT | 0 | None | 0 |
| 15 | `sub_category` | TEXT | 0 | None | 0 |
| 16 | `product_name` | TEXT | 0 | None | 0 |
| 17 | `sales` | REAL | 0 | None | 0 |
| 18 | `quantity` | INTEGER | 0 | None | 0 |
| 19 | `discount` | REAL | 0 | None | 0 |
| 20 | `profit` | REAL | 0 | None | 0 |

---

## 🎯 Step 3: Apply WHERE Filters

### Q3.1: Filter by Region = 'West' (Top 3 Samples)
```sql
SELECT order_id, customer_name, region, category, sales 
FROM superstore_sales 
WHERE region = 'West' 
LIMIT 3;
```
| Order ID | Customer Name | Region | Category | Sales |
|---|---|---|---|---|
| CA-2016-138688 | Darrin Van Huff | West | Office Supplies | 14.62 |
| CA-2014-115812 | Brosina Hoffman | West | Furniture | 48.86 |
| CA-2014-115812 | Brosina Hoffman | West | Office Supplies | 7.28 |

### Q3.2: Filter by Category = 'Technology' (Top 3 Samples)
```sql
SELECT order_id, customer_name, category, sub_category, sales 
FROM superstore_sales 
WHERE category = 'Technology' 
LIMIT 3;
```
| Order ID | Customer Name | Category | Sub-Category | Sales |
|---|---|---|---|---|
| CA-2014-115812 | Brosina Hoffman | Technology | Phones | 907.152 |
| CA-2014-115812 | Brosina Hoffman | Technology | Phones | 911.424 |
| CA-2014-143336 | Zuschuss Donatelli | Technology | Phones | 213.48 |

### Q3.3: Filter by Date (January 2017)
```sql
SELECT order_id, order_date, customer_name, sales 
FROM superstore_sales 
WHERE order_date BETWEEN '2017-01-01' AND '2017-01-31' 
LIMIT 3;
```
| Order ID | Order Date | Customer Name | Sales |
|---|---|---|---|
| CA-2017-157252 | 2017-01-20 | Cynthia Voltz | 207.846 |
| CA-2017-127432 | 2017-01-22 | Alan Dominguez | 2999.95 |
| CA-2017-127432 | 2017-01-22 | Alan Dominguez | 51.45 |

### Q3.4: Filter by Sales > $1,000
```sql
SELECT order_id, customer_name, sales, profit 
FROM superstore_sales 
WHERE sales > 1000 
LIMIT 3;
```
| Order ID | Customer Name | Sales | Profit |
|---|---|---|---|
| CA-2014-115812 | Brosina Hoffman | 1706.184 | 85.3092 |
| CA-2015-106320 | Emily Burns | 1044.63 | 240.2649 |
| US-2015-150630 | Tracy Blumstein | 3083.43 | -1665.0522 |

---

## 📊 Step 4: GROUP BY Aggregations

### Q4.1: Sales, Quantity, and Averages by Product Category
```sql
SELECT category, 
       ROUND(SUM(sales), 2) AS total_sales, 
       SUM(quantity) AS total_quantity, 
       ROUND(AVG(sales), 2) AS avg_sales, 
       ROUND(AVG(profit), 2) AS avg_profit 
FROM superstore_sales 
GROUP BY category;
```
| Category | Total Sales | Total Quantity | Avg Sales | Avg Profit |
|---|---|---|---|---|
| **Furniture** | $741,999.80 | 8,028 | $349.83 | $8.70 |
| **Office Supplies** | $719,047.03 | 22,906 | $119.32 | $20.33 |
| **Technology** | $836,154.03 | 6,939 | $452.71 | $78.75 |

> **Key Aggregation Insight**: Technology yields the highest average revenue ($452.71) and average profit ($78.75) per order. Furniture represents a large sales share ($741k) but shows a thin average profit margin ($8.70), reflecting low margins and high overhead/return rates.

---

## 📈 Step 5: Sort and Limit Results

### Q5.1: Top 5 Best-Selling Products (by Sales Value)
```sql
SELECT product_name, category, 
       ROUND(SUM(sales), 2) AS total_sales,
       SUM(quantity) AS total_qty
FROM superstore_sales 
GROUP BY product_name, category 
ORDER BY total_sales DESC 
LIMIT 5;
```
| Product Name | Category | Total Sales | Total Qty |
|---|---|---|---|
| Canon imageCLASS 2200 Advanced Copier | Technology | $61,599.82 | 20 |
| Fellowes PB500 Electric Punch... | Office Supplies | $27,453.38 | 31 |
| Cisco TelePresence System EX90... | Technology | $22,638.48 | 6 |
| HON 5400 Series Task Chairs... | Furniture | $21,870.58 | 39 |
| GBC DocuBind TL300 Electric Binding... | Office Supplies | $19,823.48 | 37 |

### Q5.2: Top 5 Most Profitable Sub-Categories
```sql
SELECT category, sub_category, 
       ROUND(SUM(profit), 2) AS total_profit 
FROM superstore_sales 
GROUP BY category, sub_category 
ORDER BY total_profit DESC 
LIMIT 5;
```
| Category | Sub-Category | Total Profit |
|---|---|---|
| Technology | **Copiers** | $55,617.82 |
| Technology | **Phones** | $44,515.73 |
| Technology | **Accessories** | $41,936.64 |
| Office Supplies | **Paper** | $34,053.57 |
| Office Supplies | **Binders** | $30,221.76 |

---

## 🎯 Step 6: Solve Business Use Cases

### Q6.1: Monthly Sales & Profit Trends (First 6 Months)
```sql
SELECT strftime('%Y-%m', order_date) AS year_month, 
       ROUND(SUM(sales), 2) AS monthly_sales, 
       ROUND(SUM(profit), 2) AS monthly_profit 
FROM superstore_sales 
GROUP BY year_month 
ORDER BY year_month 
LIMIT 6;
```
| Year-Month | Monthly Sales | Monthly Profit |
|---|---|---|
| 2014-01 | $14,236.90 | $2,450.19 |
| 2014-02 | $4,519.89 | $862.31 |
| 2014-03 | $55,691.01 | $498.73 |
| 2014-04 | $28,295.35 | $3,488.84 |
| 2014-05 | $23,648.29 | $2,738.71 |
| 2014-06 | $34,595.13 | $4,976.52 |

### Q6.2: Top 5 Customers by Lifetime Purchase Value
```sql
SELECT customer_id, customer_name, segment, 
       ROUND(SUM(sales), 2) AS total_spend,
       COUNT(DISTINCT order_id) AS order_count
FROM superstore_sales 
GROUP BY customer_id, customer_name, segment 
ORDER BY total_spend DESC 
LIMIT 5;
```
| Customer ID | Customer Name | Segment | Total Spend | Order Count |
|---|---|---|---|---|
| SM-20320 | Sean Miller | Home Office | $25,043.05 | 5 |
| TC-20980 | Tamara Chand | Corporate | $19,052.22 | 5 |
| TA-21385 | Raymond Buch | Consumer | $15,117.34 | 6 |
| KD-16270 | Karen Ferguson | Consumer | $13,617.22 | 5 |
| HL-15040 | Hunter Lopez | Consumer | $12,873.30 | 5 |

### Q6.3: Duplicate Row IDs Check (Verifying Row Uniqueness)
```sql
SELECT row_id, COUNT(*) AS count 
FROM superstore_sales 
GROUP BY row_id 
HAVING count > 1;
```
*0 rows returned.* — **Verified: No duplicate row_ids exist.**

### Q6.4: Split Order Items Check (Same Order ID and Product ID)
```sql
SELECT order_id, product_id, COUNT(*) AS count 
FROM superstore_sales 
GROUP BY order_id, product_id 
HAVING count > 1 
LIMIT 3;
```
| Order ID | Product ID | Transaction Count |
|---|---|---|
| CA-2014-100111 | OFF-PA-10000807 | 2 |
| CA-2014-110056 | TEC-AC-10002929 | 2 |
| CA-2014-118115 | OFF-BI-10001153 | 2 |

---

## 🛡️ Step 7: Data Validation & Quality Checks

### Q7.1: Row Count Validation
* **Actual Row Count in Table**: **9,994** (Matches source CSV records perfectly).

### Q7.2: Null Value Check across Critical Columns
```sql
SELECT 
    SUM(CASE WHEN row_id IS NULL THEN 1 ELSE 0 END) AS null_row_ids,
    SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) AS null_order_ids,
    SUM(CASE WHEN order_date IS NULL THEN 1 ELSE 0 END) AS null_order_dates,
    SUM(CASE WHEN customer_name IS NULL THEN 1 ELSE 0 END) AS null_customer_names,
    SUM(CASE WHEN sales IS NULL THEN 1 ELSE 0 END) AS null_sales,
    SUM(CASE WHEN profit IS NULL THEN 1 ELSE 0 END) AS null_profits
FROM superstore_sales;
```
| null_row_ids | null_order_ids | null_order_dates | null_customer_names | null_sales | null_profits |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 |

### Q7.3: Outliers & Financial Anomaly Check (Non-Positive Sales or Quantities)
```sql
SELECT COUNT(*) AS invalid_records 
FROM superstore_sales 
WHERE sales <= 0 OR quantity <= 0;
```
* **Invalid Records Count**: **0** (All rows contain positive physical and financial values).

---

## 💡 Summary of Business Insights
1. **Copiers and Phones** under the **Technology** category represent the main profitability drivers of the business.
2. **Furniture** sales are substantial ($741k) but result in extremely thin margins. Supply chain optimization, delivery rates, and discount management should be reviewed for this category.
3. We identified split order lines (same Order ID and Product ID) in the transactions. While not violating schema constraints, they represent split-shipped items or multi-package orders that must be aggregated when calculating unique transaction values.
4. **Sean Miller** ($25,043.05 spend) is our top customer by spend, representing a high-value accounts key relationship.
