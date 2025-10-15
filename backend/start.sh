#!/bin/bash
set -e
echo "🚀 Starting FastAPI app..."

# Install heavy packages at runtime
pip install --no-cache-dir torch opencv-python

# Use Railway's port if available, otherwise 8000
PORT=${PORT:-8000}

uvicorn app.main:app --host 0.0.0.0 --port $PORT