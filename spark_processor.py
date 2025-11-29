from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg, expr, stddev_samp, year, month, dayofmonth
from pyspark.sql.types import StructType, StringType, IntegerType, TimestampType

spark = SparkSession.builder \
        .appName("UPI-RealTime-Analytics") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1") \
        .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

schema = StructType() \
    .add("transaction_id", StringType()) \
    .add("timestamp", TimestampType()) \
    .add("sender_vpa", StringType()) \
    .add("amount_inr", IntegerType()) \
    .add("location", StringType()) \
    .add("app_used", StringType())

df_kafka = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "upi_transactions") \
        .option("startingOffsets", "latest") \
        .load()

df_parsed = df_kafka.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

df_windowed = df_parsed \
    .withWatermark("timestamp", "1 minute") \
    .groupBy(
        window(col("timestamp"), "5 minutes", "1 minute"),
        col("sender_vpa")
    ) \
    .agg(
        avg("amount_inr").alias("avg_spend"),
        stddev_samp("amount_inr").alias("std_dev")
    )

df_anomalies = df_windowed.withColumn(
    "upper_limit",
    col("avg_spend") + (col("std_dev") * 3)
)

df_partitioned = df_anomalies \
    .withColumn("year", year(col("window.start"))) \
    .withColumn("month", month(col("window.start"))) \
    .withColumn("day", dayofmonth(col("window.start")))

print("--- 💾 Writing Partitioned Data Lake ---")

query = df_partitioned.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "/app/data_lake/fraud_analysis") \
    .option("checkpointLocation", "/app/checkpoints/fraud_job_partitioned") \
    .partitionBy("year", "month", "day") \
    .start()

query.awaitTermination()