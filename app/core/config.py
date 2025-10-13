# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAI_API_KEY: str
    JWT_TOKEN_KEY: str
    ALGORITHM: str
    HF_HOME: str = "./model_cache"
    ALLOWED_ORIGINS: list = [
        "*",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://mellifluous-noncalculative-gwenn.ngrok-free.dev",
        "http://localhost:5173"
        ]
    
    class Config:
        env_file = ".env"

settings = Settings()