import os
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Set the JAVA_HOME environment variable to point to the Java installation
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"

# Set the PySpark submit arguments to include necessary Spark and Kafka packages
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.5.3, org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 pyspark-shell, org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3, org.apache.kafka:kafka-clients:3.2.0'

def main():
    """
    Main function to initialize a Spark session and read streaming data from Kafka,
    parse it, and write it to MongoDB.

    The application connects to a Kafka topic, processes incoming JSON data,
    and stores the results in a MongoDB collection.
    """
    
    # Initialize Spark session with specific configurations
    spark = SparkSession.builder \
        .appName("KafkaToMongo") \
        .config("spark.mongodb.output.uri", os.getenv('MONGO_URI')) \
        .config("spark.executor.memory", "4g") \
        .config("spark.driver.memory", "4g") \
        .getOrCreate()

    # Set the log level to WARN to reduce log verbosity
    spark.sparkContext.setLogLevel("WARN")

    # Define the schema of the incoming JSON data
    schema = StructType([
        StructField("date", StringType(), True),
        StructField("symbol_name", StringType(), True),
        StructField("open", DoubleType(), True),
        StructField("high", DoubleType(), True),
        StructField("low", DoubleType(), True),
        StructField("close", DoubleType(), True),
    ])

    # Read streaming data from Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", os.getenv('KAFKA_BOOTSTRAP_SERVERS')) \
        .option("subscribe", "stock_data") \
        .option("startingOffsets", "latest") \
        .load()

    # Parse the Kafka message value as JSON using the defined schema
    parsed_df = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")

    # Writing to MongoDB in batch mode (non-streaming)
    # This will save the parsed DataFrame to the specified MongoDB collection
    query = parsed_df.write \
        .format("mongo") \
        .option("uri", os.getenv('MONGO_URI')) \
        .option("collection", "stock_prices") \
        .mode("append") \
        .save()

    # Wait for the termination of the query
    query.awaitTermination()

if __name__ == "__main__":
    main()

