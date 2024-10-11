# Use the official Jupyter PySpark notebook image with Python 3.10 as the base image
FROM jupyter/pyspark-notebook:python-3.10

# Switch to root user to perform installations that require elevated permissions
USER root

# Update the package list to ensure we can access the latest versions of packages
RUN apt-get update

# Install OpenJDK 8, which is required for running Java applications
# -qq suppresses output, minimizing the verbosity of the command
RUN apt-get install openjdk-8-jdk -qq

# Install the headless version of OpenJDK 8, which is suitable for running Java without a graphical user interface
RUN apt-get install openjdk-8-jdk-headless -qq

# Set the working directory to /app, where application files will reside
WORKDIR /app

# Copy the requirements.txt file from the local machine to the working directory in the container
COPY requirements.txt .

# Install the Python dependencies listed in requirements.txt without caching to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the consumer.py script from the local machine to the working directory in the container
COPY consumer.py .

# Copy the docker-compose.yml file to the specified location for use with Airflow
COPY docker-compose.yml /home/airflow/docker-compose.yml

# Copy the docker-compose.yml file to the working directory in the container
COPY docker-compose.yml /app/docker-compose.yml

# Install hdfs-native, which may be required for interacting with HDFS (Hadoop Distributed File System)
RUN pip install hdfs-native

# Set the JAVA_HOME environment variable to the path of the installed JDK
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64

# Update the PATH environment variable to include the Java binaries
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Set the PySpark submit arguments to run Spark in local mode with 2 threads
# This allows PySpark to use the local machine for processing
RUN export PYSPARK_SUBMIT_ARGS="--master local[2] pyspark-shell"

# Command to execute when the container starts; runs the consumer.py script
CMD ["python", "consumer.py"]

