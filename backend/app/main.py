from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import routes_model, routes_user, routes_image
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

# Serve local static files (images, GIFs, etc.)
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
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

# Vision routes
app.include_router(
    routes_image.router,
    prefix = "/image",
    tags = ["Image"]
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