# Delta Lake Assignment - Incremental Processing

## About This Assignment

In this assignment, I worked on a Delta Lake workflow using Databricks.  
The dataset was first loaded, cleaned, stored as a Delta table, and then updated using incremental data.

This is a simple data engineering task where I practiced how real-time or newly received data can be merged into an existing table without recreating the full dataset again.

## What I Did

I started by reading the Superstore dataset in Databricks. Once the data was loaded, I checked the total rows, columns, and basic structure of the data.

Then I performed cleaning steps like:

- Removing duplicate records
- Handling null values
- Cleaning column names
- Trimming text values
- Fixing data types

After the cleaning part, saved the final cleaned data into a Delta table.  
To show incremental processing, I created another small dataset that had both updated records and new records.

Then used the Delta Lake MERGE command. It updated the records that were already present and inserted the new records that were not available in the table.

Then performed validation after the MERGE operation to check the final row count and duplicate records.

## SCD Type 2 Work

Along with the basic MERGE task, I also implemented SCD Type 2 for customer data.  
In this part, the old customer record is marked as inactive when any important detail changes, and a new current version is inserted.

This is useful because it keeps both old and new customer details instead of simply replacing the old data.

## Project Files

```text
delta-lake-assignment/
│
├── data/
│   └── superstore_dataset.csv
│
├── notebooks/
│   └── delta_scd_assignment.ipynb
│
├── screenshots/
│   └── delta_lake_screenshots.pdf
│
└── README.md
```

## Steps to Execute

1. Upload the dataset in Databricks.
2. Open the notebook.
3. Attach the notebook to a running cluster or serverless compute.
4. Run all cells from top to bottom.
5. Check the created Delta tables.
6. Take screenshots of important outputs.
7. Upload the notebook, screenshots, and README file to GitHub.

## Results

After completing the assignment, the Delta table contained both updated and newly inserted records.  
The validation output confirmed that duplicate row IDs were not present.  
The summary output showed the raw rows, cleaned rows, incremental rows, and final table rows.

## Final Note

This assignment gave me practical understanding of Delta Lake, especially how MERGE is used in incremental data loading. It also helped me understand why SCD Type 2 is important when we need to track old and new versions of records.
