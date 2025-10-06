from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_flight, routes_model, routes_voice
from app.core.config import settings

app = FastAPI(
    title="AI Chatbot API",
    description="LLM-powered chatbot with flight info, voice, and multi-model support",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.ALLOWED_ORIGINS,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# # Routers
# app.include_router(routes_flight.router, prefix="/flight", tags=["Flight"])
# app.include_router(routes_model.router, prefix="/model", tags=["Model"])
# app.include_router(routes_voice.router, prefix="/voice", tags=["Voice"])

@app.get("/")
def root():
    return {"message": "Welcome to the AI Chatbot!"}