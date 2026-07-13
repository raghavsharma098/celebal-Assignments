# E-Commerce Order Analytics System

This project is an end-to-end data analytics system designed to process and analyze e-commerce order data using Python and SQL. It demonstrates data generation, cleaning, SQLite integration, complex SQL aggregations, and a command-line reporting tool.

## Features

- **Data Generation:** Synthetic dataset creation with realistic inconsistencies (e.g., missing values, invalid formats) using Python's `Faker` library.
- **Data Cleaning:** Data normalization, type casting, validation, and integrity checks using `pandas`.
- **Database Architecture:** A normalized SQLite database with constraints (Primary Keys, Foreign Keys) ensuring referential integrity.
- **SQL Analytics:** Comprehensive analytics spanning basic aggregations, window functions (Ranking, Running Totals, LAG/LEAD), Cohort Analysis, and NTILE Segmentation.
- **Reporting CLI:** A Python command-line utility to generate dynamic summary reports.

## Project Structure

```text
ecommerce-analytics-system/
│── data/
│   ├── raw/                 # Raw data with intentional errors
│   └── cleaned/             # Processed and cleaned datasets
│── scripts/
│   ├── generate_data.py     # Script to generate raw data
│   ├── clean_data.py        # Script to clean raw data
│   ├── load_data.py         # Script to create DB schema and load data
│   ├── report_cli.py        # CLI reporting tool
│   └── test_cases.py        # Edge case validation script
│── sql/
│   ├── schema.sql           # Database table definitions
│   ├── aggregations.sql     # Basic and intermediate analytics
│   ├── window_functions.sql # Advanced analytics with window functions
│   └── cohort_analysis.sql  # Complex CTE cohort analysis
│── output/
│   └── sample_reports/      # Example outputs from the CLI
│── README.md
```

## Setup & Execution

### Prerequisites

Ensure you have Python 3.8+ installed. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 1. Data Generation

Generate the raw datasets (with intentional inconsistencies):

```bash
python scripts/generate_data.py
```

### 2. Data Cleaning

Clean the raw data. This script will print an anomaly report and save cleaned CSV files in `data/cleaned/`.

```bash
python scripts/clean_data.py
```

### 3. Database Initialization

Create the SQLite database schema and load the cleaned data into `ecommerce.db`:

```bash
python scripts/load_data.py
```

### 4. Running the Reporting CLI

The CLI tool supports various reports and date range summaries. 

Run a predefined report:
```bash
python scripts/report_cli.py --report revenue
python scripts/report_cli.py --report top_customers
python scripts/report_cli.py --report retention
```

Run a dynamic summary report for a specific period:
```bash
python scripts/report_cli.py --start-date 2025-01-01 --end-date 2026-06-01 --period monthly
```

### 5. Running Tests

To verify edge-case handling (e.g., referential integrity blocks on invalid items):

```bash
python scripts/test_cases.py
```

## SQL Analytics Queries

The project contains several SQL files inside the `sql/` directory answering complex business questions:
- **`aggregations.sql`**: Revenue per category, top customers, month-wise trends, return rates.
- **`window_functions.sql`**: Running totals, `DENSE_RANK`, YoY comparisons, segmenting by lifetime value using `NTILE`, and frequently bought together items.
- **`cohort_analysis.sql`**: Cohort tracking and monthly retention rates.
