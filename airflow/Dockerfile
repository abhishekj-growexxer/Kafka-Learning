# airflow/Dockerfile

# Use the official Apache Airflow image as the base image.
# Version 2.5.1 is specified to ensure a stable environment.
FROM apache/airflow:2.5.1

# Switch to the root user to install system packages.
USER root

# Install prerequisites for Docker installation.
# This includes:
# - apt-transport-https: allows APT to use HTTPS for repositories.
# - ca-certificates: ensures that the system can verify SSL certificates.
# - curl: a tool to transfer data from or to a server.
# - gnupg: allows the use of GPG keys.
# - lsb-release: provides Linux Standard Base information about the system.
RUN apt-get update && \
    apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release && \
    # Clean up APT cache to reduce the image size.
    rm -rf /var/lib/apt/lists/*

# Add Docker’s official GPG key for Debian to verify the packages.
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up the Docker stable repository for Debian.
# This allows the installation of Docker from the official Docker repository.
RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine and Docker CLI along with Containerd (a container runtime).
RUN apt-get update && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    # Clean up APT cache again to reduce the image size.
    rm -rf /var/lib/apt/lists/*

# Install Docker Compose (if not included in the above installation).
# The version specified here is 2.20.2.
RUN curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    # Make the Docker Compose binary executable.
    chmod +x /usr/local/bin/docker-compose

# Check if the 'docker' group exists; if not, create it.
# Then add the 'airflow' user to the 'docker' group, allowing it to run Docker commands.
RUN if ! getent group docker; then groupadd docker; fi && usermod -aG docker airflow

# Switch back to the airflow user to run Airflow processes with limited privileges.
USER airflow

# Set the working directory to the home of the airflow user.
WORKDIR /home/airflow

# Copy the Python dependencies list into the working directory.
COPY requirements.txt /home/airflow/requirements.txt

# Install Python dependencies specified in requirements.txt without caching.
RUN pip install --no-cache-dir -r /home/airflow/requirements.txt

# (Optional) Copy the docker-compose.yml file if it exists in the context.
# This file can be used to define and run multi-container Docker applications.
COPY docker-compose.yml /home/airflow/docker-compose.yml

