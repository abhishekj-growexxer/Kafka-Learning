from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',  # Owner of the DAG
    'depends_on_past': False,  # Don't wait for past runs to succeed
    'email': ['your_email@example.com'],  # Email to notify on failure
    'email_on_failure': False,  # Disable email on failure
    'email_on_retry': False,  # Disable email on retry
    'retries': 1,  # Number of retries on failure
    'retry_delay': timedelta(minutes=5),  # Delay between retries
}

# Define the DAG context
with DAG(
    'kafka_pipeline_dag',  # Unique identifier for the DAG
    default_args=default_args,  # Default arguments for the tasks
    description='A DAG to manage Kafka pipeline',  # Brief description of the DAG
    schedule_interval=timedelta(minutes=1),  # Schedule to run every minute
    start_date=datetime(2024, 1, 1),  # Start date for the DAG runs
    catchup=False,  # Don't backfill the DAG runs
) as dag:

    # Task to check the status of the Kafka producer container
    check_producer = BashOperator(
        task_id='check_producer',  # Unique identifier for the task
        bash_command='docker-compose ps | grep producer',  # Command to check producer status
        cwd='/home/airflow/'  # Working directory for the command
    )

    # Task to check the status of the Kafka consumer container
    check_consumer = BashOperator(
        task_id='check_consumer',  # Unique identifier for the task
        bash_command='docker-compose ps | grep consumer',  # Command to check consumer status
        cwd='/home/airflow/'  # Working directory for the command
    )

    # Task to check the status of the MongoDB container
    check_mongo = BashOperator(
        task_id='check_mongo',  # Unique identifier for the task
        bash_command='docker-compose ps | grep mongo',  # Command to check MongoDB status
        cwd='/home/airflow/'  # Working directory for the command
    )

    # Task to check the status of the Kafka broker container
    check_kafka = BashOperator(
        task_id='check_kafka',  # Unique identifier for the task
        bash_command='docker-compose ps | grep kafka',  # Command to check Kafka status
        cwd='/home/airflow/'  # Working directory for the command
    )

    # Define the task dependencies
    # The tasks will execute in the following order:
    # 1. check_producer
    # 2. check_consumer
    # 3. check_mongo
    # 4. check_kafka
    check_producer >> check_consumer >> check_mongo >> check_kafka

