# Use the official Python 3.10 slim image as the base image.
# This version is lightweight and designed for efficiency.
FROM python:3.10-slim

# Set the working directory to /app.
# All subsequent commands will be executed in this directory.
WORKDIR /app

# Copy the requirements.txt file to the current working directory (/app).
# This file lists the Python dependencies needed for the application.
COPY requirements.txt .

# Install the Python dependencies listed in requirements.txt.
# --no-cache-dir option prevents caching of package installations,
# which helps to reduce the image size.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the docker-compose.yml file to the specified location in the container.
# This file is typically used to define and run multi-container Docker applications.
# Here, it is copied to /home/airflow/docker-compose.yml, possibly for use in a specific context.
COPY docker-compose.yml /home/airflow/docker-compose.yml

# Copy the same docker-compose.yml file to the working directory (/app).
# This may be needed for local development or testing within the /app context.
COPY docker-compose.yml /app/docker-compose.yml

# Copy the producer.py script into the working directory.
# This script is expected to contain the main logic for the application.
COPY producer.py .

# Define the command to run when the container starts.
# This will execute the producer.py script using the Python interpreter.
CMD ["python", "producer.py"]

