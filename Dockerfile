# Use the official Python 3.8 slim image as the base image
FROM python:3.8-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Set the PYTHONPATH environment variable to include common and server_side directories
ENV PYTHONPATH="/app/common:/app/server_side:${PYTHONPATH}"

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the common directory to the working directory
COPY common ./common

# Copy the server_side directory to the working directory
COPY server_side ./server_side

# Specify the command to run the server when the container starts
CMD ["python", "server_side/server.py"]
