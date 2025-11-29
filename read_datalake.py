from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("DataLakeReader") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("--- 📁 Reading from Data Lake ---")

try:
    df = spark.read.parquet("/app/data_lake/fraud_analysis")

    count = df.count()
    print(f"Total Rows found: {count}")

    df.show(truncate=False)

except Exception as e:
    print("No data found yet! (Did you wait for watermark?)")
    print(f"Error: {e}")