# Base image
FROM python:3.10-slim

# Set environment variables to ensure non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install necessary system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements file first for better caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app into the container
COPY . /app/

# Expose the Flask port
EXPOSE 5000

# Default command to run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]
