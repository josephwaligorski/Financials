# backend/Dockerfile
# This Dockerfile now uses an entrypoint script for a more robust startup process.

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install curl for the healthcheck to work
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code, including the new entrypoint script
COPY . .

# Make the entrypoint script executable
RUN chmod +x ./entrypoint.sh

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variables needed for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Set the entrypoint script to be executed when the container starts.
ENTRYPOINT ["./entrypoint.sh"]
