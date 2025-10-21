#!/bin/bash
set -e
echo "🚀 Starting FastAPI app..."

# Railway assigns PORT dynamically
PORT=${PORT:-8080}

# Ensure torch is installed (runtime safety)
pip show torch >/dev/null 2>&1 || pip install torch==2.2.2+cpu --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu

# Run FastAPI
uvicorn app.main:app --host 0.0.0.0 --port $PORT