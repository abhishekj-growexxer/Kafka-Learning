#!/bin/bash

# This script sets up a Docker environment for a Kafka messaging system.
# It brings up the necessary Docker containers, waits for Kafka to become ready,
# and creates a Kafka topic for stock data.

# Bring up Docker containers in detached mode
# The -d flag runs the containers in the background.
docker-compose up -d

# Wait for Kafka to be ready
# Since Kafka may take some time to initialize, we pause the script for 20 seconds.
echo "Waiting for Kafka to be ready..."
sleep 20

# Create Kafka topics if not using the kafka-topics service
# This command creates a new Kafka topic named 'stock_data'.
# - --topic stock_data: Specifies the name of the topic to be created.
# - --bootstrap-server kafka:9092: Points to the Kafka server for connection.
# - --partitions 3: Defines the number of partitions for the topic, allowing parallel processing.
# - --replication-factor 1: Sets the number of replicas for the topic, providing fault tolerance.
docker exec kafka kafka-topics --create --topic stock_data --bootstrap-server kafka:9092 --partitions 3 --replication-factor 1

# Notify the user that the pipeline is up and running
echo "Pipeline is up and running."
