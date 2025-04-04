FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy front-end files
COPY contents/ .

# Install dependencies
RUN python3 -m pip install --no-cache-dir --upgrade pip Flask requests

# Unbuffer Python
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Run Flask server
CMD ["python", "server.py"]
