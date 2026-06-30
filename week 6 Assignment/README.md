# Week 6 Spark Assignment

## Objective

This assignment is based on understanding Spark architecture and using PySpark for basic data processing.
The main focus is on reading data, handling schema, applying transformations, filtering records, working with CSV/Parquet formats, and saving the processed output.

## Topics Covered

* Spark Architecture
* Driver, Cluster Manager, and Executors
* Client Mode and Cluster Mode
* Lazy Evaluation
* DAG / Lineage Graph
* Transformations and Actions
* CSV and Parquet file formats
* Predicate Pushdown
* Filtering and selecting columns
* Renaming columns
* Type casting
* Adding new columns
* Handling null values
* Writing output in CSV and Parquet format

## Project Structure

```text
Week6_Spark_Assignment/
│
├── data/
│   └── source.csv
│
├── output/
│
├── week6_pyspark_code.py
│
└── README.md
```

## Dataset Used

For this assignment, I have used a local CSV dataset stored inside the `data` folder.

Dataset path used in the code:

```text
data/source.csv
```

The dataset contains the columns required for performing filtering, selection, schema handling, transformations, and output writing.

## Tools and Technologies Used

* Python
* PySpark
* Apache Spark
* CSV file format
* Parquet file format
* VS Code / Jupyter Notebook

## How to Run the Code

First, keep the dataset inside the `data` folder with the name:

```text
source.csv
```

Then open the terminal in the project folder and run:

```bash
python week6_pyspark_code.py
```

Or using Spark submit:

```bash
spark-submit week6_pyspark_code.py
```

## Main Steps Performed in Code

### 1. Created Spark Session

A SparkSession is created to start the Spark application.

### 2. Read CSV File

The CSV file is read using header and inferSchema options.

```python
df = spark.read.csv("data/source.csv", header=True, inferSchema=True)
```

### 3. Checked Schema

The schema of the dataset is checked using:

```python
df.printSchema()
```

### 4. Displayed Sample Records

Only a few records are displayed using:

```python
df.show(5)
```

This is safer than using `collect()` because `collect()` brings all data to the driver.

### 5. Selected Required Columns

Only useful columns were selected from the dataset for further processing.

### 6. Applied Filters

Filtering conditions were applied based on the requirement, such as category, amount, region, or priority.

### 7. Modified DataFrame

The DataFrame was modified by renaming columns, casting data types, and adding new calculated columns.

### 8. Handled Null Values

Rows having null values in important columns were removed using filter conditions.

### 9. Saved Output

The final processed data was saved in both CSV and Parquet format.

```python
cleaned_df.write.mode("overwrite").option("header", True).csv("output/cleaned_csv")
cleaned_df.write.mode("overwrite").parquet("output/cleaned_parquet")
```

## Output Generated

The program generates processed output inside the `output` folder.

Expected output folders:

```text
output/
│
├── cleaned_csv/
│
└── cleaned_parquet/
```

## Performance Insights

Spark improves performance by using lazy evaluation. It does not execute transformations immediately. Instead, it prepares an optimized execution plan and runs it only when an action is called.

Parquet is better than CSV for large datasets because it stores data in columnar format. This helps Spark read only the required columns and reduces unnecessary data loading.

Predicate Pushdown also improves performance because Spark can apply filters while reading the data, especially in Parquet format. This reduces memory usage and speeds up processing.

For large datasets, it is better to use `.show(5)` instead of `.collect()` because `.collect()` brings the complete data to the driver and can cause memory issues.

## Conclusion

In this assignment, I learned how Spark processes large datasets efficiently using transformations, actions, lazy evaluation, and optimized file formats. I also understood how Spark architecture works with Driver, Cluster Manager, and Executors. The practical part helped me understand how to build a basic Spark pipeline from reading data to saving processed output.
