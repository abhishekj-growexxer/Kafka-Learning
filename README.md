# Kafka-Learning

Kafka-Based Data Pipeline Project
=================================

This project implements a Kafka-based real-time data pipeline for stock market data. It involves generating, consuming, processing, and monitoring data using technologies like Kafka, Spark, MongoDB, Docker, and Prometheus. Apache Airflow is used to orchestrate the data pipeline.

Project Gist
------------

*   Generate real-time stock data using a Kafka producer.
*   Consume and process data using PySpark.
*   Store processed data in MongoDB.
*   Monitor the system using Prometheus.
*   Orchestrate the pipeline using Apache Airflow.
*   Deploy all services using Docker Compose.

### Key Technologies Used

*   Apache Kafka
*   PySpark
*   MongoDB
*   Apache Airflow
*   Prometheus
*   Docker & Docker Compose

Steps to Run the Project
------------------------

### Step 1: Clone the Repository

`git clone https://github.com/abhishekj-growexxer/Kafka-Learning.git && cd Kafka-Learning`

### Step 2: Set Up and Run the Project

Give the necessary executable permissions and run the setup script:

`chmod +x setup.sh   ./setup.sh`

### Step 3: Access the Services

*   Airflow Web UI: `http://localhost:8080`
*   Prometheus Web UI: `http://localhost:9090`

### Step 4: Monitor Logs

To monitor the producer and consumer logs:

`docker-compose logs -f producer   docker-compose logs -f consumer`

### Step 5: Verify Data in MongoDB

Use a MongoDB client or command-line tool to verify that stock data is being stored:

*   Database: `kafka_db`
*   Collection: `stock_prices`

### Step 6: Troubleshooting and Enhancements

If you encounter any issues, refer to the **Challenges Faced** and **Solutions** sections in the report.

### Future Enhancements

*   Introduce fault tolerance and retry mechanisms for Kafka consumer.
*   Implement data validation before processing.
*   Integrate Grafana with Prometheus for better visualizations.

Conclusion
----------

This project demonstrates the power of real-time data pipelines using Kafka and Spark, integrated with modern containerization techniques using Docker and orchestration with Airflow. The project provides a robust foundation for further exploration into big data processing and scalable architectures.
