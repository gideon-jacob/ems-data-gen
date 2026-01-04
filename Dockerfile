# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install basic tools
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Copy the dependency file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create start script to run both processes concurrently
RUN echo '#!/bin/bash\npython data_gen.py &\npython cloud_worker.py' > /app/start.sh && chmod +x /app/start.sh

# Run the start script when the container launches
CMD ["/app/start.sh"]
