from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_flight, routes_model, routes_voice
from app.core.config import settings
from app.services.llm_service import LLMService
from app.models.request_models import LLMRequest
from dotenv import load_dotenv
from app.database.db_session import connect_db, disconnect_db
from contextlib import asynccontextmanager

load_dotenv()

llm_service = LLMService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()          # ✅ connect before any request
    yield
    await disconnect_db()       # ✅ disconnect on shutdown

app = FastAPI(
    title="AI Chatbot API",
    description="LLM-powered chatbot with flight info, voice, and multi-model support",
    version="1.0.0",
    lifespan=lifespan
)

# Routes

# Model Routes
app.include_router(
    routes_model.router,
    prefix = "/model",
    tags = ["LLM"]
)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.ALLOWED_ORIGINS,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/")
def root():
    return {"message": "Welcome to the AI Chatbot!"}