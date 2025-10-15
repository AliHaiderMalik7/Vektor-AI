# Use small Python image
FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install system dependencies
RUN apk add --no-cache \
    build-base \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

# Copy the rest of the app
COPY . .

# Make start script executable
RUN chmod +x start.sh

# Expose FastAPI port
EXPOSE 8000

# Run using sh (Alpine doesn't have bash)
CMD ["sh", "start.sh"]
