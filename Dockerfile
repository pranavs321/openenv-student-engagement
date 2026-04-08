FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirement first for layer caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the working directory contents
COPY . /app/

# Environment constraints are 2vCPU / 8GB RAM, this slim image is well within limits
# By default, the environment relies mostly on API calls which consume negligible memory.
