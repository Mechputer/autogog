# Use a lightweight Python image
FROM base:latest

# Set a working directory
WORKDIR /app

# Copy model files into the container (adjust path to your folder structure)
COPY contents/ .

# Unbuffer Python
ENV PYTHONUNBUFFERED=1

# Expose the port your app will run on (adjust per container)
EXPOSE 5000

# Command to run the API server
CMD ["/bin/bash", "-c", "python model.py"]
