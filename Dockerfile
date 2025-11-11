# Use a slim Python base image
FROM python:3.10-slim

# Install system dependencies (Tesseract + zbar + basic tools)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libzbar0 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Copy Python dependencies first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY . .

# Expose port 8080 (Heroku, Fly.io, Cloud Run usually expect 8080)
EXPOSE 8080

# Run with Gunicorn in production
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]