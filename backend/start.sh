#!/bin/bash
set -e
echo "🚀 Starting FastAPI app..."

# Railway assigns PORT dynamically
PORT=${PORT:-8080}

# Run FastAPI
uvicorn app.main:app --host 0.0.0.0 --port $PORT