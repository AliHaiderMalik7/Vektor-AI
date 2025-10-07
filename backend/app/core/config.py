# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    ALLOWED_ORIGINS: list = [
        "*",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://mellifluous-noncalculative-gwenn.ngrok-free.dev"
        ]
    
    class Config:
        env_file = ".env"

settings = Settings()