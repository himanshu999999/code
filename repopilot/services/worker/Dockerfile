FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Add packages to PYTHONPATH
ENV PYTHONPATH=/app:/packages/shared:/packages/evals

# Run Celery worker
CMD ["celery", "-A", "celery_app", "worker", "--loglevel=info", "--concurrency=2"]
