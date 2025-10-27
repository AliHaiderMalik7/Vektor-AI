from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_model, routes_user
from app.core.config import settings
from app.services.llm_service import LLMService
from app.models.request_models import LLMRequest
from dotenv import load_dotenv

load_dotenv()

llm_service = LLMService()

app = FastAPI(
    title="AI Chatbot API",
    description="LLM-powered chatbot for Fitness Assistant.",
    version="1.0.0"
)

# Routes

# Model Routes
app.include_router(
    routes_model.router,
    prefix = "/model",
    tags = ["LLM"]
)

# User routes
app.include_router(
    routes_user.router,
    prefix = "/user",
    tags = ["User"]
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
    return {"message": "Welcome to the Fitness AI Chatbot!"}