from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, sum as spark_sum, min as spark_min, max as spark_max, trim
from pyspark.sql.types import TimestampType

# Create Spark Session
spark = SparkSession.builder \
    .appName("Week 5 Spark Assignment") \
    .getOrCreate()

# Sample data for assignment practice
data = [
    (1, "2026-06-01", "West", "Electronics", 5000.0, "Jaipur", 22, "Premium", "Active", "2026-06-01 10:30:00", "user1@gmail.com", "user1", 5000.0, "S1"),
    (1, "2026-06-01", "West", "Electronics", 5000.0, "Jaipur", 22, "Premium", "Active", "2026-06-01 10:30:00", "user1@gmail.com", "user1", 5000.0, "S1"),
    (2, "2026-06-02", "West", "Clothing", 1500.0, "Jaipur", 25, "Basic", None, "2026-06-02 12:00:00", "user2@gmail.com", "user2", None, "S1"),
    (3, "2026-06-03", "East", "Electronics", 7000.0, "Bikaner", 19, "Premium", "Active", "2026-06-03 09:15:00", None, "user3", 7000.0, "S2"),
    (4, "2026-06-04", "South", "Grocery", 800.0, "Jodhpur", 31, "Premium", None, "2026-06-04 11:45:00", "user4@gmail.com", "", 800.0, "S2"),
    (5, "2026-06-05", "West", "Grocery", 1200.0, "Jaipur", 28, "Premium", "Active", "2026-06-05 14:20:00", "user5@gmail.com", "user5", 1200.0, "S3"),
]

columns = [
    "user_id", "transaction_date", "region", "product_category", "sale_amount",
    "city", "age", "subscription", "status", "raw_timestamp",
    "email", "username", "price", "store_id"
]

df = spark.createDataFrame(data, columns)

# Extra data only to show city count greater than 100
extra_data = []
for i in range(6, 112):
    extra_data.append(
        (i, "2026-06-06", "North", "Grocery", 500.0, "Jaipur", 24, "Premium",
         "Active", "2026-06-06 10:00:00", f"user{i}@gmail.com", f"user{i}", 500.0, "S1")
    )

df_extra = spark.createDataFrame(extra_data, columns)
df = df.union(df_extra)

print("\nOriginal Data:")
df.show(10, truncate=False)

print("\nOriginal Schema:")
df.printSchema()


# Q3: Remove duplicate rows based on user_id and transaction_date
df_no_duplicates = df.dropDuplicates(["user_id", "transaction_date"])

print("\nAfter Removing Duplicates Based on user_id and transaction_date:")
df_no_duplicates.show(10, truncate=False)


# Q4: Filter region West and group by product_category to find average sale_amount
west_avg_sales = df.filter(col("region") == "West") \
    .groupBy("product_category") \
    .agg(avg("sale_amount").alias("average_sale_amount"))

print("\nAverage Sale Amount for West Region by Product Category:")
west_avg_sales.show()


# Q5: Fill null values in status column with Unknown
df_status_filled = df.na.fill({"status": "Unknown"})

print("\nAfter Filling Null Status with Unknown:")
df_status_filled.select("user_id", "status").show(10)


# Q6: Count records for each city where count is greater than 100
city_count = df.groupBy("city") \
    .agg(count("*").alias("total_records")) \
    .filter(col("total_records") > 100)

print("\nCities Having Record Count Greater Than 100:")
city_count.show()


# Q8: Filter age between 18 and 30 and subscription Premium
premium_age_filter = df.filter(
    (col("age") >= 18) &
    (col("age") <= 30) &
    (col("subscription") == "Premium")
)

print("\nUsers with Age Between 18 and 30 and Premium Subscription:")
premium_age_filter.select("user_id", "age", "subscription").show(10)


# Q10: Cast raw_timestamp to TimestampType and rename it to event_time
df_timestamp = df.withColumn(
    "raw_timestamp",
    col("raw_timestamp").cast(TimestampType())
).withColumnRenamed("raw_timestamp", "event_time")

print("\nAfter Casting raw_timestamp to TimestampType and Renaming to event_time:")
df_timestamp.select("user_id", "event_time").show(10, truncate=False)

print("\nUpdated Schema:")
df_timestamp.printSchema()


# Q12: Remove rows where email is null OR username is empty
df_email_clean = df.filter(
    (col("email").isNotNull()) &
    (trim(col("username")) != "")
)

print("\nAfter Removing Rows with Null Email or Empty Username:")
df_email_clean.select("user_id", "email", "username").show(10, truncate=False)


# Q13: Calculate min, max and mean of price column
price_stats = df.agg(
    spark_min("price").alias("minimum_price"),
    spark_max("price").alias("maximum_price"),
    avg("price").alias("mean_price")
)

print("\nPrice Statistics:")
price_stats.show()


# Q15: Final processing pipeline
# 1. Remove duplicates
# 2. Fill null prices with 0
# 3. Group by store_id and calculate total revenue

final_result = df.dropDuplicates() \
    .na.fill({"price": 0}) \
    .groupBy("store_id") \
    .agg(spark_sum("price").alias("total_revenue"))

print("\nFinal Processing Pipeline Result - Total Revenue by Store:")
final_result.show()


# Stop Spark Session
spark.stop()