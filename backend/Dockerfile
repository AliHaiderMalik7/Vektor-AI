# Use official Python image (small and fast)
FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir -r requirements.txt \
    && apk add --no-cache build-base \
    && rm -rf /root/.cache/pip

# Copy the rest of your app
COPY . .

# Make sure your start script can run
RUN chmod +x start.sh

# Expose port for FastAPI
EXPOSE 8000

# Run your app via start.sh
CMD ["bash", "start.sh"]
