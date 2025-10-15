#!/bin/sh
set -e
echo "🚀 Starting FastAPI app..."

# Use Railway's port if available, otherwise 8000
PORT=${PORT:-8000}
# echo "Using PORT=$PORT"

uvicorn app.main:app --host 0.0.0.0 --port $PORT
