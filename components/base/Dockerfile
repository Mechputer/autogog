# Use a lightweight Python image
FROM python:3.8-slim

# Set a working directory
WORKDIR /app

# Install system-level dependencies
RUN apt-get update && apt-get install -y \
    apt-utils \
    build-essential \
    wget \
    && apt-get clean

# Install and upgrade Python dependencies
RUN python3 -m pip install --no-cache-dir --upgrade pip flask torch transformers safetensors

# Add a dummy file to prevent cache invalidation in future builds
RUN echo "Base image built on $(date)" > /build_info.txt
