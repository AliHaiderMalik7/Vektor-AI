echo "🚀 Starting FastAPI app on Railway..."
# Install dependencies
pip install -r requirements.txt
# Starting FastAPI application
uvicorn app.main:app --host 0.0.0.0 --port $PORT