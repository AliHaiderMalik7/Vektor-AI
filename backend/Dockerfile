# Use small Python image
FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Copy only requirements first (cache optimization)
COPY requirements.txt .

# Install system tools + Python dependencies
RUN apk add --no-cache gcc g++ musl-dev libffi-dev make \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

RUN pip install --no-cache-dir -r requirements.txt \
    && find / -type d -name '__pycache__' -exec rm -rf {} + || true


# Copy the rest of your app
COPY . .

# Make start script executable
RUN chmod +x start.sh

# Expose FastAPI port
EXPOSE 8000

# Run app using sh (not bash)
CMD ["sh", "start.sh"]
