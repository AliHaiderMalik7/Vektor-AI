from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_flight, routes_model, routes_voice
from app.core.config import settings
from app.services.llm_service import LLMService
from app.models.request_models import LLMRequest

llm_service = LLMService()

app = FastAPI(
    title="AI Chatbot API",
    description="LLM-powered chatbot with flight info, voice, and multi-model support",
    version="1.0.0"
)

# Routes

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