#!/bin/bash
set -e
echo "🚀 Starting FastAPI app on Railway..."
# Install dependencies
pip install -r requirements.txt
# Starting FastAPI application
PORT=${PORT:-8000}
uvicorn app.main:app --host 0.0.0.0 --port $PORT